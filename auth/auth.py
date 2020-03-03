import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from db import get_db

auth_page = Blueprint("auth", __name__, url_prefix="/auth")
'''

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
''' 


# регистрация нового пользователя
@auth_page.route("/register", methods=("GET", "POST"))
def register():

    # !!! ДОДЕЛАТЬ ВАЛИДАЦИЮ

    if request.method == "POST":
        db = get_db()
        message = None

        first_name = request.form["first_name"].strip()
        last_name = request.form["last_name"].strip()
        birsday = request.form["birsday"]
        email = request.form["email"].strip()
        gender = request.form['gender']

        # if not birsday: birsday = 'NULL'
        # if not birsday: birsday = 'NULL'

        if not first_name:
            message = "Введите имя"
        if not last_name:
            message = "Введите фамилию"
        if not email:
            message = "Введите email"
        if not birsday:
            birsday = None
        if not gender:
            gender = None
        
        # if message is not None:
        #     flash(message)
        #     return redirect(url_for('index'))
        
        # проверка наличия введенного email в БД
        # если email есть, Пользователь считается зарестрированным
        if not db.is_exist_email(email):
            try:
                db.add_new_user((first_name, last_name, email, gender, birsday))
                # session['data'] = (first_name, last_name, email, gender, birsday, repr(type(birsday)))
            except Exception as err:
                flash(repr(err))
                return redirect(url_for('index'))
        
            
               
        session['logged_in'] = True
        session['user'] = first_name + ' ' + last_name

        return redirect(url_for('index'))
