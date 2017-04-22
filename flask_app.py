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


@app.route('/onboard', methods=['GET', 'POST'])
def onboard():
    if not logged_in():
        return redirect(url_for('login'))

        # if db.session.query(db.exists().where(Sender.id == get_user_info('id'))).scalar():
        #     # Already onboarded, take to index
        #     return redirect(url_for('index'))
        #
        # if request.method != 'POST':
        #     # Send form
        #     return render_template('onboard.html', first=get_user_info('given_name'), error='')
        #
        # error = ''
        # if request.form['phone'] == '':
        #     error = '<li>phone number is empty</li>'
        # if request.form['driver'] == 'yes':
        #     if request.form['homezip'] == '':
        #         error += '<li>home zip is empty</li>'
        #     if request.form['workzip'] == '':
        #         error += '<li>work zip is empty</li>'
        #     if request.form['caryear'] == '':
        #         error += '<li>car year is empty</li>'
        #     if request.form['carmake'] == '':
        #         error += '<li>car make is empty</li>'
        #     if request.form['carmodel'] == '':
        #         error += '<li>car model is empty</li>'
        #     if request.form['carcolor'] == '':
        #         error += '<li>car color is empty</li>'
        #     if request.form['carplate'] == '':
        #         error += '<li>car license plate is empty</li>'
        # if error != '':
        #     error = '<ul>' + error + '</ul>'
        #     return render_template('onboard.html', first=get_user_info('given_name'), error=error)
        #
        # s = Sender()
        # s.first = get_user_info('given_name')
        # s.last = get_user_info('family_name')
        # s.id = get_user_info('id')
        # s.phone = request.form['phone']
        # s.num_ratings = 1
        # s.rating = 3.5
        # db.session.add(s)
        # db.session.commit()
        #
        # if request.form['driver'] == 'yes':
        #     c = Car()
        #     c.color = request.form['carcolor']
        #     c.make = request.form['carmake']
        #     c.model = request.form['carmodel']
        #     c.year = request.form['caryear']
        #     c.plate = request.form['carplate']
        #     c.owner_id = get_user_info('id')
        #     db.session.add(c)
        #     db.session.commit()
        #
        #     d = Driver()
        #     d.first = get_user_info('given_name')
        #     d.last = get_user_info('family_name')
        #     d.id = get_user_info('id')
        #     d.phone = request.form['phone']
        #     d.num_ratings = 1
        #     d.rating = 3.5
        #     d.home_zip = request.form['homezip']
        #     d.work_zip = request.form['workzip']
        #     d.car_id = c.id
        #     db.session.add(d)
        #     db.session.commit()
        #
        # return redirect(url_for('index'))


@app.route('/login')
def login():
    if logged_in():
        return redirect(url_for('index'))
    return render_template('login.html')


@app.route('/signup')
def signup():
    if logged_in():
        return redirect(url_for('index'))
    return 'signup'


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
