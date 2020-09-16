from flask import Flask, session, redirect, url_for, request
from markupsafe import escape
import os
import requests

app = Flask(__name__)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = os.environ.get('SESSION_SECRET')

@app.route('/')
def index():
    prompt = ""
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

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
    return str(items.json())

@app.route('/create_account', methods=['POST'])
def make_account():
    return redirect('http://users/api/v1.0/create_user')

@app.route('/create_item', methods=['POST'])
def make_item():
    return redirect('http://items/api/v1.0/add_item')