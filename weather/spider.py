# http://www.gismeteo.ua/city/daily/5093/

# список температур
# response.xpath('//div[@class="widget__body"]//div[@class="value"]/span[contains(@class, "_c")]/text()').extract()

# список давление в мм.рт.ст
# response.xpath("//div[contains(@class, 'chart__pressure')]//span[contains(@class, 'mm_hg_atm')]/text()").extract()

# список значений влажности
# response.xpath("//div[contains(@class, 'widget__row_humidity')]//div[contains(@class, 'w_humidity_type_')]/text()").extract()

# список значений скорости ветра в м/с
# response.xpath("//div[contains(@class, 'row_wind-or-gust')]//span[contains(@class, 'wind_m_s')]/text()").extract()

# список значений наличия осадков
# response.xpath("//div[contains(@class, 'row_precipitation')]//span[contains(@class, 'text_lowercase')]/text()").extract()

from scrapy import Spider
from scrapy.crawler import CrawlerProcess
import json
import config


class WeatherSpider(Spider):
    name = "weather_spider"
    start_urls = [
        'http://www.gismeteo.ua/city/daily/5093/',
    ]

    def parse(self, response):

        for widget in response.xpath('//div[@class="__frame_sm"]'):

            temps = widget.xpath(
                '//div[@class="widget__body"]//div[@class="value"]/span[contains(@class, "_c")]/text()').extract()
            pressure = widget.xpath(
                "//div[contains(@class, 'chart__pressure')]//span[contains(@class, 'mm_hg_atm')]/text()").extract()
            humidity = widget.xpath(
                "//div[contains(@class, 'widget__row_humidity')]//div[contains(@class, 'w_humidity_type_')]/text()").extract()
            wind_speed = widget.xpath(
                "//div[contains(@class, 'row_wind-or-gust')]//span[contains(@class, 'wind_m_s')]/text()").extract()
            precipitation = widget.xpath(
                "//div[contains(@class, 'row_precipitation')]//span[contains(@class, 'text_lowercase')]/text()").extract()
            
            yield {
                'time': list(range(2, 24, 3)),
                'temperature': temps,
                'pressure': pressure,
                'humidity': humidity,
                'wind_speed': [ws.strip() for ws in wind_speed],
                'precipitation': precipitation,
            }

"""Запись данных в файл. Данные перезаписуются при каждом запуске паука"""
class JsonWriterPipeline(object):

    def open_spider(self, spider):
        self.file = open(config.SOURCE_DATA_FILE, 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item))
        self.file.write(line)
        return item



if __name__ == "__main__":

    process = CrawlerProcess(settings={
        "ITEM_PIPELINES": {"spider.JsonWriterPipeline": 10},
    })

    process.crawl(WeatherSpider)
    process.start()

    with open('weather/weather.json', 'r') as source:
            weather_data = json.load(source)
    print(weather_data)


