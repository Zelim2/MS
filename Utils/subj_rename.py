# libraries
import json
import pandas as pd

def rename_subj(
    df: pd.DataFrame,
    column: str,
    subj_rename_data: dict
) -> pd.DataFrame:
    subj_rename_data = subj_rename_data.copy()
    # переименовывает регионы в соответствии с конфигом (приводит к общему стандарту)
    # для унификации датафреймов и корректного отображения их на карте
    while len(subj_rename_data) != 0:
        for correct_name in subj_rename_data.keys():
            for wrong_name in subj_rename_data[correct_name]:
                if wrong_name in tuple(df[column]):
                    df[column].replace(wrong_name, correct_name, inplace=True)
                    break
            subj_rename_data.pop(correct_name)
            break
    return df

