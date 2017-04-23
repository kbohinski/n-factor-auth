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


@app.route('/nfa', methods=['GET', 'POST'])
def nfa():
    # if request.method == 'POST':
    return render_template('nfa.html')


@app.route('/onboard', methods=['GET', 'POST'])
def onboard():
    if not logged_in():
        return redirect(url_for('index'))

    if request.method == 'POST':
        method = 'api'

        if 'numbers' in request.form:
            # Team Based
            method = 'team'
            numbers = request.form['numbers'].split(',')
            users.update({'email': session['email']}, {'$set': {'method': method, 'numbers': numbers}})

        if 'n' in request.form:
            # N
            method = 'n'
            n = request.form['n'].split(',')[0]
            number = request.form['n'].split(',')[1]
            users.update({'email': session['email']}, {'$set': {'method': method, 'number': number, 'n': n}})

            users.update({'email': session['email']}, {'$set': {'method': method}})

            return redirect(url_for('logout'))

    return render_template('onboard.html')


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
            users.insert_one(user)
            session['email'] = request.form['email']
            return redirect(url_for('onboard'))

        if request.form['submit'] == 'login':
            row = users.find_one({'email': request.form['email']})
            if pwd_context.verify(request.form['pass'], row['pass']):
                session['email'] = row['email']
                return redirect(url_for('nfa'))
            return redirect(url_for('index'))

    # If we havent returned yet theres an error
    return jsonify({'error': 'we aren\'t sure what happened...'})


@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))


def logged_in():
    if 'email' in session:
        return True
    return False


if __name__ == '__main__':
    app.run()
