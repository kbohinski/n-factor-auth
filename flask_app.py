import json

import requests
from pymongo import MongoClient
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from passlib.apps import custom_app_context as pwd_context

app = Flask(__name__)
app.config.from_pyfile('config.py')

client = MongoClient()
db = client['n-factor-auth']
users = db['users']


@app.route('/')
def index():
    if not logged_in():
        return render_template('index.html', logged_in=False, first='')
    return render_template('index.html', logged_in=True, first=session['info']['first'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    if logged_in():
        return redirect(url_for('index'))

    if request.method == 'POST':
        if request.form['submit'] == 'signup':
            # lol
            return 'signup'
        if request.form['submit'] == 'login':
            # lol
            return 'login'


@app.route('/logout')
def logout():
    session.pop('info', None)
    session.pop('logged_in', None)
    session.pop('n', None)
    return redirect(url_for('index'))


def logged_in():
    if 'logged_in' in session:
        return True
    return False


if __name__ == '__main__':
    app.run()
