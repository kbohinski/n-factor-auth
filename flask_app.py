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
    return render_template('index.html', logged_in=logged_in())


@app.route('/login', methods=['GET', 'POST'])
def login():
    if logged_in():
        return redirect(url_for('index'))

    if request.method == 'POST':
        if request.form['submit'] == 'signup':
            user = {
                'email': request.form['email'],
                'pass': pwd_context.hash(request.form['pass'])
            }
            id = users.insert_one(user).inserted_id
            session['info'] = {'id': id, 'email': request.form['email']}
            return redirect(url_for('onboard'))

        if request.form['submit'] == 'login':
            row = users.find_one({'email': request.form['email']})
            if pwd_context.verify(request.form['pass'], row['pass']):
                session['info'] = {'id': row['id'], 'email': row['email']}
                return redirect(url_for('nfa'))
            return redirect(url_for('index'))

    # If we havent returned yet theres an error
    return jsonify({'error': 'we aren\'t sure what happened...'})


@app.route('/logout')
def logout():
    session.pop('info', None)
    session.pop('n', None)

    return redirect(url_for('index'))


def logged_in():
    if 'logged_in' in session:
        return True
    return False


if __name__ == '__main__':
    app.run()
