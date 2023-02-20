#!pip install pillow
#!pip install selenium

import io

from PIL import Image
from selenium import webdriver

import folium

def map_to_png(
    Map: folium.folium.Map, 
    config: dict,
    name: str="image.png"
) -> None:
    path = config["Driver"]["selenium_path"]
    
    options = webdriver.firefox.options.Options()
    driver = webdriver.Firefox(
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