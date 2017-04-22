import json

import requests
from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)


class Driver(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.String(32), primary_key=True)
    first = db.Column(db.String(256))
    last = db.Column(db.String(256))
    phone = db.Column(db.String(14))
    home_zip = db.Column(db.Integer)
    work_zip = db.Column(db.Integer)
    car_id = db.Column(db.Integer)
    num_ratings = db.Column(db.Integer)
    rating = db.Column(db.Float)


class Sender(db.Model):
    __tablename__ = 'senders'

    id = db.Column(db.String(32), primary_key=True)
    first = db.Column(db.String(256))
    last = db.Column(db.String(256))
    phone = db.Column(db.String(14))
    num_ratings = db.Column(db.Integer)
    rating = db.Column(db.Float)


class Car(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_id = db.Column(db.String(32))
    make = db.Column(db.String(32))
    model = db.Column(db.String(32))
    year = db.Column(db.Integer)
    color = db.Column(db.String(32))
    plate = db.Column(db.String(6))


oauth = OAuth(app)

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_ID'),
    consumer_secret=app.config.get('GOOGLE_SECRET'),
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v2/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)


# {
#   "data": {
#     "email": "kbohinski@gmail.com",
#     "family_name": "Bohinski",
#     "given_name": "Kevin",
#     "id": "1043...",
#     "link": "https://plus.google.com/+KevinBohinski0",
#     "name": "Kevin Bohinski",
#     "picture": "https://lh5.googleusercontent.com/--W5XH_3FNxo/AAAAAAAAAAI/AAAAAAAAJ6M/62eSheVjhH8/photo.jpg",
#     "verified_email": true
#   }
# }


@app.route('/')
def index():
    if not logged_in():
        return render_template('index.html', logged_in=False, first='')
    return render_template('index.html', logged_in=True, first=get_user_info('given_name'))


@app.route('/onboard', methods=['GET', 'POST'])
def onboard():
    if not logged_in():
        return redirect(url_for('login'))

    if db.session.query(db.exists().where(Sender.id == get_user_info('id'))).scalar():
        # Already onboarded, take to index
        return redirect(url_for('index'))

    if request.method != 'POST':
        # Send form
        return render_template('onboard.html', first=get_user_info('given_name'), error='')

    error = ''
    if request.form['phone'] == '':
        error = '<li>phone number is empty</li>'
    if request.form['driver'] == 'yes':
        if request.form['homezip'] == '':
            error += '<li>home zip is empty</li>'
        if request.form['workzip'] == '':
            error += '<li>work zip is empty</li>'
        if request.form['caryear'] == '':
            error += '<li>car year is empty</li>'
        if request.form['carmake'] == '':
            error += '<li>car make is empty</li>'
        if request.form['carmodel'] == '':
            error += '<li>car model is empty</li>'
        if request.form['carcolor'] == '':
            error += '<li>car color is empty</li>'
        if request.form['carplate'] == '':
            error += '<li>car license plate is empty</li>'
    if error != '':
        error = '<ul>' + error + '</ul>'
        return render_template('onboard.html', first=get_user_info('given_name'), error=error)

    s = Sender()
    s.first = get_user_info('given_name')
    s.last = get_user_info('family_name')
    s.id = get_user_info('id')
    s.phone = request.form['phone']
    s.num_ratings = 1
    s.rating = 3.5
    db.session.add(s)
    db.session.commit()

    if request.form['driver'] == 'yes':
        c = Car()
        c.color = request.form['carcolor']
        c.make = request.form['carmake']
        c.model = request.form['carmodel']
        c.year = request.form['caryear']
        c.plate = request.form['carplate']
        c.owner_id = get_user_info('id')
        db.session.add(c)
        db.session.commit()

        d = Driver()
        d.first = get_user_info('given_name')
        d.last = get_user_info('family_name')
        d.id = get_user_info('id')
        d.phone = request.form['phone']
        d.num_ratings = 1
        d.rating = 3.5
        d.home_zip = request.form['homezip']
        d.work_zip = request.form['workzip']
        d.car_id = c.id
        db.session.add(d)
        db.session.commit()

    return redirect(url_for('index'))


@app.route('/login')
def login():
    if logged_in():
        return redirect(url_for('index'))
    return google.authorize(callback=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    session.pop('google_token', None)
    session.pop('user_info', None)
    return redirect(url_for('index'))


@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    if db.session.query(db.exists().where(Driver.id == get_user_info('id'))).scalar():
        # Already registered, send to dash...
        session['user_type'] = 'sender'
        return redirect(url_for('index'))
    if db.session.query(db.exists().where(Sender.id == get_user_info('id'))).scalar():
        # Already registered, send to dash...
        session['user_type'] = 'driver'
        return redirect(url_for('index'))
    # Not registered yet!
    return redirect(url_for('onboard'))


@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')


def logged_in():
    if 'google_token' in session:
        return True
    return False


def get_user_info(key):
    if not logged_in():
        return redirect(url_for('login'))
    if 'user_info' not in session:
        session['user_info'] = google.get('userinfo').data
    return session['user_info'][key]


if __name__ == '__main__':
    app.run()
