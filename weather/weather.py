from flask import Flask
from flask import g
from flask import session
from flask import render_template
from flask import request
from flask import Blueprint
from flask import redirect
from flask import url_for
from jinja2 import TemplateNotFound

TEMPLATES_DIR = 'weather/'

weather_page = Blueprint('weather', __name__, 
                     template_folder='templates', url_prefix='/weather')


@weather_page.route('')
def weather_show():
    # забрать данные от скрапера
    if not session['logged_in']:
        return redirect(url_for('index'))
    return render_template(TEMPLATES_DIR + 'weather.html')