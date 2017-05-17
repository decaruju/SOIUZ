from flask import Flask, render_template, request, session, redirect, url_for
from flask_pymongo import PyMongo
from flask_session import Session
from hashlib import sha512

app = Flask(__name__)
mongo = PyMongo(app)

from flask import request, session, flash

def _pass_hash(string, salt):
    sha = sha512()
    sha.update((string + salt).encode('utf-8'))
    for _ in range(1000):
        sha.update(sha.hexdigest().encode('utf-8'))
    return sha.hexdigest()

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    if request.method == 'POST':
        user = users.find_one({'username': request.form['username']})
        if user and user['password'] == _pass_hash(request.form['pass'], request.form['username']):
            session['username'] = request.form['username']
            flash('Login complete')
            return redirect(url_for('index'))
        return 'Connection refusée'
    return 'oups'

@app.route('/register', methods=['POST'])
def register():
    users = mongo.db.users
    if request.method == 'POST':
        user = users.find_one({'username': request.form['username']})
        print(user)
        if not user:
            if not check_password(request.form['pass']):
                return 'incorrect password'
            users.insert({'username': request.form['username'],
                          'password': _pass_hash(request.form['pass'], request.form['username'])})
            flash('Registration complete')
            redirect(url_for('index'))
    return ''

def check_password(password):
    return True

@app.route('/')
def index():
    if 'username' in session:
        return 'you are logged in as' + session['username']
    return render_template('index.html')

@app.route('/register_page')
def register_page():
    return render_template('register.html')

if __name__ == '__main__':
    app.add_url_rule('/login', login, methods=['POST'])
    app.add_url_rule('/register', register, methods=['POST'])
    app.secret_key = 'paulio'
    app.config['SESSION_TYPE'] = 'mongodb'
    sess = Session()
    sess.init_app(app)

    app.run()
