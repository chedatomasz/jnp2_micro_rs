from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
import os
import time
import psycopg2

#before anything wait for postgres to come alive

start_time = time.time()
timeout = 5
sleep_time = 1

dbname = os.environ.get('POSTGRES_DB')
dbuser = os.environ.get('POSTGRES_USER')
dbpassword = os.environ.get('POSTGRES_PASSWORD')
dbhost = os.environ.get('POSTGRES_HOST')


while (time.time() - start_time < timeout):
    try:
        conn = psycopg2.connect(dbname=dbname, user=dbuser, password=dbpassword, host=dbhost)
        print("Postgres is ready!")
        conn.close()
        break
    except psycopg2.OperationalError:
        print(f"Postgres isn't ready. Waiting for {sleep_time} seconds...")
        time.sleep(sleep_time)




app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{dbuser}:{dbpassword}@{dbhost}/{dbname}'


db = SQLAlchemy(app)



class User(db.Model):
    username = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)    

db.create_all()


@app.route('/api/v1.0/get_token', methods=['POST'])
def get_token():
    data = request.json
    
    if data is None or not 'username' in data or not 'password' in data:
        return 'Incorrect data', 400

    u = User.query.get(data['username'])

    if not u or u.password != data['password']:
        return 'Incorrect login or password', 403

    token = jwt.encode({'username': data['username']}, os.environ.get('JWT_SECRET'), algorithm='HS256')
    token = token.decode()
    return jsonify({'token': token}), 200

@app.route('/api/v1.0/create_user', methods=['POST'])
def create_user():
    data = request.json
    
    if data is None or not 'username' in data or not 'password' in data:
        return 'Incorrect data', 400

    previous_user = User.query.get(data['username'])

    if previous_user:
        return 'User already exists', 403

    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify("Added"), 200

@app.route('/identify', methods=['GET'])
def identify():
    return 'User service', 200