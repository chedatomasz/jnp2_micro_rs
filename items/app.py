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



class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    description = db.Column(db.String(512))


    def __repr__(self):
        return '<Item {}>'.format(self.id)    

db.create_all()


@app.route('/api/v1.0/get_item_data/<id>', methods=['GET'])
def get_item_data(id):

    item = Item.query.get(id)

    if item is None:
        return 'Item not found', 404

    return jsonify({'id': item.id, 'name': item.name, 'description': item.description}), 200

@app.route('/api/v1.0/add_item', methods=['POST'])
def create_item():
    data = request.json
    
    if data is None or not 'name' in data or not 'description' in data:
        return 'Incorrect data', 400

    new_item = Item(name=data['name'], description=data['description'])
    db.session.add(new_item)
    db.session.commit()

    return jsonify({'id' : new_item.id}), 200

@app.route('/api/v1.0/all_items', methods=['GET'])
def all_items():
    items = Item.query.all()

    return jsonify([i.id for i in items]), 200

@app.route('/identify', methods=['GET'])
def identify():
    return 'Item service', 200
