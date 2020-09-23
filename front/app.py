from flask import Flask, session, redirect, url_for, request
from markupsafe import escape
import os
import requests

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.environ.get('SESSION_SECRET')

@app.route('/')
def index():
    if 'username' in session:
        return '''
        Logged in as {}'
        <a href='/logout'> Log out </a>
        <a href='/rate'> Rate items </a>
        <a href='/items'> View items </a>
        <a href='/create_item'> Create item </a>
        '''.format(escape(session['username']))
    return '''You are not logged in
    <a href='/create_account'> Sign up </a>
    <a href='/login'> Sign in </a>
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        reply = requests.post('http://users/api/v1.0/get_token', json = {"username": username, "password": password})
        if reply.status_code == 200:
            session['username'] = request.form['username']
            session['token'] = reply.json()['token']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('token', None)
    return redirect(url_for('index'))


@app.route('/rate', methods=['GET', 'POST'])
def rate():
    if request.method == 'POST':
        item_id = request.form['item_id']
        rating = request.form['rating']
        payload = {
            "token": session['token'],
            "item_id": item_id,
            "rating_value": rating
        }
        reply = requests.post('http://ratings/api/v1.0/add_rating', json = payload)
        return redirect(url_for('index'))
    return '''
        <h1> Rate item </h1>
        <form method="post">
            <p><input type=text name=item_id>
            <p><input type=number name=rating>
            <p><input type=submit value=Rate>
        </form>
    '''

@app.route('/item/<item_id>', methods=['GET'])
def see_item(item_id):
    description = requests.get(f'http://items/api/v1.0/get_item_data/{item_id}')
    ratings = requests.get(f'http://ratings/api/v1.0/get_item_ratings/{item_id}')
    recommended = requests.get(f'http://recommendations/api/v1.0/get_item_recommendations/{item_id}')
    return "ITEM " + str(description.json()) + "WITH RATINGS " + str(ratings.json()) + "SIMILAR TO " + str(recommended.json())

@app.route('/items', methods=['GET'])
def see_items():
    items = requests.get('http://items/api/v1.0/all_items')
    rows = ['''<a href='/item/{}'> Item {} </a> <br>'''.format(item_id, item_id) for item_id in items.json()]


    return ' '.join(rows)

@app.route('/create_account', methods=['GET', 'POST'])
def make_account():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        payload = {
            "username": username,
            "password": password
        }
        reply = requests.post('http://users/api/v1.0/create_user', json = payload)
        return redirect(url_for('index'))
    return '''
        <h1> Create account </h1>
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Create>
        </form>
    '''

@app.route('/create_item', methods=['GET', 'POST'])
def make_item():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        payload = {
            "token": session['token'],
            "name": name,
            "description": description
        }
        reply = requests.post('http://items/api/v1.0/add_item', json = payload)
        return redirect(url_for('index'))
    return '''
        <h1> Create item </h1>
        <form method="post">
            <p><input type=text name=name>
            <p><input type=text name=description>
            <p><input type=submit value=Create>
        </form>
    '''