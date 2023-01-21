"""
ИСПОЛЬЗОВАТЬ ФАЙЛ ТОЛЬКО ПРИ ОБНОВЛЕНИИ ОНЛАЙН json-ИСТОЧНИКОВ!
АКТУАЛЬНЫЙ json лежит в файле "geo_data.json"

Обработка онлайн json-файлов с данными по РФ (полигоны для отображения на картах) и загрузка данных в файл geo_data.json
Исходные ссылки:

№1 (весит много, есть Крым и г. Севастополь)
https://raw.githubusercontent.com/tttdddnet/Python-Jupyter-Geo/88f57d23e1a7fdc283eec9e255fd0a2dc3103e12/geo_ru.json

№2 (весит мало, её будем использовать как основную, нет Крыма и г. Севастополь)
https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/russia.geojson
"""

# libraries
import json
from urllib import request

# Ссылки на два онлайн-источника полигонов, которые можно отобразить на карте
# Нужны для последующего их объединения, тк в разных конфигах не хватает некоторых регионов
URL_large = "https://raw.githubusercontent.com/tttdddnet/Python-Jupyter-Geo/88f57d23e1a7fdc283eec9e255fd0a2dc3103e12/geo_ru.json"
URL_opt = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/russia.geojson"


# Функции

def clear_dict(
    rf_subj_data: dict
) -> dict:
    # очищает ненужные поля в словаре, чтобы не использовать их в дальнейшем при создании df
    
    # из основного json-а
    rf_subj_data["properties"].pop("cartodb_id", None)
    rf_subj_data["properties"].pop("created_at", None)
    rf_subj_data["properties"].pop("updated_at", None)
    rf_subj_data["properties"].pop("name_latin", None)
    
    # из большого json-а
    rf_subj_data["properties"].pop("id", None)
    rf_subj_data["properties"].pop("Subject_translit", None)
    rf_subj_data["properties"].pop("Subject_en", None)
    
    return rf_subj_data


def check_subj(
    rf_subj_data: dict,
    region_name_list: list
) -> dict:
    # Выбирает из большого конфига только нужные субъекты 
    # Для последующего присоединения к основному json-у
    
    if rf_subj_data["properties"]["name"] in region_name_list:
        return rf_subj_data


if __name__ == "__main__":
    with request.urlopen(URL_opt) as file:
        geo_data = json.load(file)
    
    with request.urlopen(URL_large) as file:
        geo_data_large = json.load(file)
    
    # Задаём список регионов, который включим потом из большого json-а в осноной
    region_name_list = [
        "Sevastopol'",
        "Crimea"
    ]
    
    # Лист словарей с данными для каждого региона из region_name_list
    # Для последующего присоединения к основному json-у
    region_data_list = list(
        filter(
            lambda x: check_subj(x, region_name_list),
            geo_data_large['features']
        )
    )
    
    
    # дополнение основного словаря отсутствующими регионами
    geo_data['features'].extend(region_data_list)
    
    # Очистка всех ненужных столбцов в словаре
    # Чтобы при последующем импорте не отображать в df их
    list(map(lambda x: clear_dict(x), geo_data['features']))


    # запись файла в json
    # В дальнейшем именно этот файл будет служить основой для отображения на карте
    with open("geo_data.json", "w", encoding="utf-8") as file:
        json.dump(geo_data, file, ensure_ascii=False)

    
    # Проверка
    #with open("geo_data.json", encoding="utf-8") as file:
    #    data = json.load(file)
    #
    #data['features'][-1]['properties']
