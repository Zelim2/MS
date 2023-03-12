#!pip install pillow
#!pip install selenium

import io

from PIL import Image
from selenium import webdriver

import folium

def map_to_png(
    Map: folium.folium.Map, 
    config: dict,
    name: str="image.png",
    driver_name: "str - Firefox / Yandex"="Firefox"
) -> None:
    path = config["Driver"][driver_name]
    if driver_name == "Firefox":
        options = webdriver.firefox.options.Options()
        driver = webdriver.Firefox(
            path,
            options=options
        )
    elif driver_name == "Yandex":
        path = config["Driver"][driver_name]
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(
            path,
            options=options
        )
    
    Map._png_image = None
    Map._to_png(
        delay=5, 
        driver=driver
    )
    
    img = Image.open(io.BytesIO(Map._png_image))
    img.save(name)