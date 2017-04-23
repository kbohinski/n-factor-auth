import random
import string

from flask import Flask, render_template, redirect, url_for, request, session, jsonify
from passlib.apps import custom_app_context as pwd_context
from pymongo import MongoClient
from twilio.rest import Client

app = Flask(__name__)
app.config.from_pyfile('config.py')

client = MongoClient()
db = client['n-factor-auth']
users = db['users']

twilio = Client(app.config.get('TWILIO_ID'), app.config.get('TWILIO_TOKEN'))


@app.route('/')
def index():
    if logged_in():
        if passed_nfa():
            return redirect(url_for('index'))
        return redirect(url_for('nfa'))
    return render_template('index.html', logged_in=logged_in())


@app.route('/nfa', methods=['GET', 'POST'])
def nfa():
    if not logged_in():
        return redirect(url_for('index'))

    if logged_in() and passed_nfa():
        return redirect(url_for('index'))

    if request.method == 'POST':
        if session['mongo']['method'] == 'n':
            for i in range(0, int(session['mongo']['n'])):
                if session[str('tokens' + str(i))] != request.form[str('tokens' + str(i))]:
                    session['error'] = '<p>one of your tokens was wrong, try again</p>'
                    return redirect(url_for('nfa'))
            return redirect(url_for('index'))

    if session['mongo']['method'] == 'n':
        for i in range(0, int(session['mongo']['n'])):
            token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            session[str('tokens' + str(i))] = token
            twilio.messages.create(to=session['mongo']['number'], from_=app.config.get('TWILIO_NUMBER'), body=token)

    return render_template('nfa.html', error=session['error'], n=int(session['mongo']['n']))


@app.route('/onboard', methods=['GET', 'POST'])
def onboard():
    if not logged_in():
        return redirect(url_for('index'))

    if logged_in() and passed_nfa():
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
        if passed_nfa():
            return redirect(url_for('index'))
        return redirect(url_for('nfa'))

    if request.method == 'POST':
        session['error'] = ''

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
                row.pop('_id', None)
                session['mongo'] = row
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


def passed_nfa():
    if 'nfa_passed' in session:
        return True
    return False


if __name__ == '__main__':
    app.run()
