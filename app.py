from flask import Flask
from flask import g
from flask import session
from flask import render_template
from flask import request

from feedback.feedback import feedback_page
from weather.weather import weather_page
from auth.auth import auth_page
from db import close_db


app = Flask(__name__)
app.config.from_pyfile('config.py')

# регистрация bluprint
app.register_blueprint(feedback_page)
app.register_blueprint(weather_page)
app.register_blueprint(auth_page)

app.teardown_appcontext(close_db)

# Функция first_function выполняется до первого запроса приложению
@app.before_first_request
def first_function():
    # очистка сессии
    session.clear()
    # флаг регистрации
    session['logged_in'] = False



# главная страница
@app.route('/')
def index():
    with app.app_context():
        return render_template('index.html')
if __name__ == "__main__":
    app.run()