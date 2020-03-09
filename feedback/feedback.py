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
from auth.auth import is_valid_email, is_valid_name
from auth.auth import login_required

TEMPLATES_DIR = 'feedback/'

feedback_page = Blueprint('feedback', __name__, 
                     template_folder='templates', url_prefix='/feedback')


@feedback_page.route('/')
@login_required
def feedback():
    return render_template(TEMPLATES_DIR + 'feedback.html')


@feedback_page.route('/add', methods=['POST'])
def feedback_add():
    """Функция проверяет введенные данные и добавляет новое сообщение в БД"""
    if request.method == 'POST':
        db = get_db()

        name = request.form['name']
        email = request.form['email']
        text = request.form['text']

        if not is_valid_name(name):
            flash("Некорректное имя")
        elif not is_valid_email(email):
            flash("Некорректный email")
        elif not text:
            flash("Введите текст сообщения")
        else:
            try:
                db.add_new_feedback((name, email, text), session['user']['id'])
            except:
                flash('Ошибка. Попробуйте еще раз')
            else: 
                flash('Сообщение отправлено!')
    
    return redirect(url_for('feedback.feedback'))


@feedback_page.route('/list')
@login_required
def feedback_list_show():
    """Выводит страницу с последними 10ю сообщениями"""
    db = get_db()
    feedback_list = db.get_list_feedback()
    return render_template(TEMPLATES_DIR + 'feedback_list.html', feedback_list=feedback_list)
