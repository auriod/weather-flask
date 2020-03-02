from flask import Flask
from flask import g
from flask import session
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import url_for
from flask import Blueprint
from jinja2 import TemplateNotFound

TEMPLATES_DIR = 'feedback/'
feedback_list = []

feedback_page = Blueprint('feedback', __name__, 
                     template_folder='templates', url_prefix='/feedback')


@feedback_page.route('/')
def feedback():
    g.feedback_list = []
    return render_template(TEMPLATES_DIR + 'feedback.html')


@feedback_page.route('/add', methods=['POST'])
def feedback_add():
    global feedback_list
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        text = request.form['text']
        feedback_list.append([name, email, text])
        message = "Сообщение отправлено"
        flash(message)
    return redirect(url_for('feedback.feedback'))


@feedback_page.route('/list')
def feedback_list_show():
    # собрать с БД все отзывы - сохранить в переменнную отправить в шаблон
    if session['logged_in']:
        return render_template(TEMPLATES_DIR + 'feedback_list.html', feedback_list=feedback_list)
    else:
        return redirect(url_for('index'))
