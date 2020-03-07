import functools
import re

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from db import get_db

auth_page = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """Декоратор проверяет зарегистрирован ли пользователь"""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not session['logged_in']:
            return redirect(url_for("index"))

        return view(**kwargs)

    return wrapped_view


def is_valid_name(name):
    """Валидация имени и фамилии. Одно слово, без пробелов, только кириллица"""
    reg = r"^[а-я]+$"
    return bool(re.match(reg, name.lower()))


def is_valid_email(email):
    """Валидация email по шаблону name@example.com"""
    reg = r'^[a-z0-9_-]+@[a-z]+\.[a-z]{2,6}$'
    return bool(re.match(reg, email, flags=re.I))


def is_valid_bisday(birsday):
    """Валидация даты рождения. Формат ГГГГ-ММ-ДД"""
    reg = r'^\d{4}-\d\d-\d\d$'
    return bool(re.match(reg, birsday))


# регистрация нового пользователя
@auth_page.route("/register", methods=("GET", "POST"))
def register():

    if request.method == "POST":
        db = get_db()
        message = None

        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        email = request.form["email"].strip()
        birsday = request.form["birsday"]
        gender = request.form['gender']


        if not is_valid_name(first_name):
            message = "Некорректное имя"
        if not is_valid_name(last_name):
            message = "Некорректная фамилия"
        if not is_valid_email(email):
            message = "Некорректный email"
        if not birsday:
            birsday = None
        elif not is_valid_bisday(birsday):
            message = 'Некорректная дата рождения' 
        if not gender:
            gender = None
        
        if message is not None:
            flash(messga)
            return redirect(url_for('index'))

    # проверка наличия введенного email в БД
    # если email есть, Пользователь считается зарестрированным
    if not db.is_exist_email(email):
        try:
            id_user = db.add_new_user((first_name, last_name, email, gender, birsday))
        except Exception as err:
            flash(repr(err))
            return redirect(url_for('index'))
    else:
        id_user = db.get_data_user(email)[0]
        
            
    session['logged_in'] = True
    session['user'] = {
        'username': ' '.join([last_name, first_name]),
        'email': email,
        'id': id_user,
    }

    return redirect(url_for('index'))
