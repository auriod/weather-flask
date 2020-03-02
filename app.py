from flask import Flask
from flask import g
from flask import session
from flask import render_template
from flask import request

from feedback.feedback import feedback_page
from weather.weather import weather_page
from auth.auth import auth_page


app = Flask(__name__)
app.config.from_pyfile('config.py')

app.register_blueprint(feedback_page)
app.register_blueprint(weather_page)
app.register_blueprint(auth_page)

# Функция first_function выполняется до первого запроса приложению
@app.before_first_request
def first_function():
    session.clear()
    session['logged_in'] = False


@app.route('/')
def index():
    with app.app_context():
        return render_template('index.html')

if __name__ == "__main__":
    app.run()