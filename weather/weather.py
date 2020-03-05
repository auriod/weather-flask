import json
from threading import Thread
from multiprocessing import Process

from flask import Flask
from flask import g
from flask import session
from flask import render_template
from flask import request
from flask import Blueprint
from flask import redirect
from flask import url_for
from flask import flash
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner

from .spider import WeatherSpider
import config
from auth.auth import login_required


TEMPLATES_DIR = 'weather/'

weather_page = Blueprint('weather', __name__, 
                     template_folder='templates', url_prefix='/weather')

@weather_page.before_request
# процесс для запуска и перезапуска реактора реактора
def run_reactor():
    p = Process(target=start_spider)
    p.start()
    p.join()

# функция запускает паука
def start_spider():
        runner = CrawlerRunner(settings=config.SETTING_SPIDER)
        d = runner.crawl(WeatherSpider)
        d.addBoth(lambda _: reactor.stop())
        reactor.run(installSignalHandlers=False)


@weather_page.route('')
@login_required
def weather_show():
    weather_data = []

    try:
        with open(config.SOURCE_DATA_FILE, 'r') as source:
            weather_data = json.load(source)
    except FileNotFoundError:
        flash("Ошибка. Данные отсутствуют.")

    return render_template(TEMPLATES_DIR + 'weather.html', weather_data=weather_data)

if __name__ == "__main__":
    with open('weather/weather.json', 'r') as s:
        data = json.load(s)
    print(data)