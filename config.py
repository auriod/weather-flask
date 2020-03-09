"""ФАЙЛ КОНФИГУРАЦИИ"""
DEBUG = True
SECRET_KEY = b'\xe2\xe3=\xb8 )j\xf1\x15\xaa-\xadBHf\x8c\xd4n:\x98\x0eb\x93\x8c'

# DATABASE SETTING
CONFIG_DATABASE = {
    'user': 'root',
    'password': '47458973',
    'host':'localhost',
    'port': '3306',
    'buffered':True,
}
DATABASE = 'weather_zp_app'

# SPIDER SETTING
SOURCE_DATA_FILE = 'weather/weather.json'
SETTING_SPIDER = {
    "ITEM_PIPELINES": {"weather.spider.JsonWriterPipeline": 10},
}
