from flask import Flask, render_template, request
from flask_script import Manager, Command, Shell
from flask import Flask, render_template, request, redirect, url_for, flash, make_response, session
import datetime

app = Flask(__name__)
app.permanent_session_lifetime = datetime.timedelta(days=365)
app = Flask(__name__, template_folder="templates")
app.debug = True
app.config['SECRET_KEY'] = 'a really really really really long secret key'

manager = Manager(app)

class Faker(Command):
    'Команда для добавления поддельных данных в таблицы'
    def run(self):
        # логика функции
        print("Fake data entered")

manager.add_command("faker", Faker())

@app.route('/article/', methods=['POST',  'GET'])
def article():
    if request.method == 'POST':
        print(request.form)
        res = make_response("")
        res.set_cookie("font", request.form.get('font'), 60*60*24*15)
        res.headers['location'] = url_for('article')
        return res, 302
    return render_template('article.html')

@app.route('/cookie/')
def cookie():
    if not request.cookies.get('foo'):
        res = make_response("Setting a cookie")
        res.set_cookie('foo', 'bar', max_age=60*60*24*365*2)
    else:
	    res = make_response("Value of cookie foo is {}".format(request.cookies.get('foo')))


@app.route('/delete-cookie/')
def delete_cookie():
    res = make_response("Cookie Removed")
    res.set_cookie('foo', 'bar', max_age=0)
    return res

def shell_context():
    import os, sys
    return dict(app=app, os=os, sys=sys)

@app.route('/visits-counter/')
def visits():
    if 'visits' in session:
        session['visits'] = session.get('visits') + 1  # чтение и обновление данных сессии
    else:
        session['visits'] = 1  # настройка данных сессии
    return "Total visits: {}".format(session.get('visits'))

@app.route('/delete-visits/')
def delete_visits():
    session.pop('visits', None)  # удаление данных о посещениях
    return 'Visits deleted'



manager.add_command("shell", Shell(make_context=shell_context))

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login/', methods=['post', 'get'])
def login():

    message = ''

    if request.method == 'POST':
        password = request.form.get('password')
        username = request.form.get('username')

    if username == 'root' and password == 'pass':
        message = "Correct username and password"

    else:
        message = "Wrong username or password"

    return render_template('login.html', message=message)

@app.route('/session/')
def updating_session():
    res = str(session.items())

    cart_item = {'pineapples': '10', 'apples': '20', 'mangoes': '30'}
    if 'cart_item' in session:
        session['cart_item']['pineapples'] = '100'
        session.modified = True
    else:
        session['cart_item'] = cart_item
    return res

@app.route('/user//')
def user_profile(user_id):
    return "Profile page of user #{}".format(user_id)

@app.route('/books//')
def books(genre):
    return "All Books in {} category".format(genre)


if __name__ == "__main__":
    app.run()
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT=int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT= 5555
    app.run(HOST, PORT)
