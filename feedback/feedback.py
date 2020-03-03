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

from db import get_db

TEMPLATES_DIR = 'feedback/'

feedback_page = Blueprint('feedback', __name__, 
                     template_folder='templates', url_prefix='/feedback')


@feedback_page.route('/')
def feedback():
    g.feedback_list = []
    return render_template(TEMPLATES_DIR + 'feedback.html')


@feedback_page.route('/add', methods=['POST'])
def feedback_add():

    def return_with_message(message):
        """Возвращает к странице ввода сообщения c сообщением"""
        flash(message)
        return redirect(url_for('feedback.feedback'))

    if request.method == 'POST':
        db = get_db()

        name = request.form['name']
        email = request.form['email']
        text = request.form['text']

    if not name:
        flash("Введите имя")
    elif not email:
        flash("Введите email")
    elif not text:
        flash("Введите текст сообщения")
    else:
        try:
            db.add_new_feedback((name, email, text))
        except:
            flash('Ошибка. Попробуйте еще раз')
        else: 
            flash('Сообщение отправлено!')
    
    return redirect(url_for('feedback.feedback'))


@feedback_page.route('/list')
def feedback_list_show():
    # собрать с БД все отзывы - сохранить в переменнную отправить в шаблон
    db = get_db()
    feedback_list = db.get_list_feedback()
    if session['logged_in']:
        return render_template(TEMPLATES_DIR + 'feedback_list.html', feedback_list=feedback_list)
    else:
        return redirect(url_for('index'))
