from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import jwt
import os
import time
import psycopg2
import pika

#before anything wait for postgres to come alive

start_time = time.time()
timeout = 5
sleep_time = 1

dbname = os.environ.get('POSTGRES_DB')
dbuser = os.environ.get('POSTGRES_USER')
dbpassword = os.environ.get('POSTGRES_PASSWORD')
dbhost = os.environ.get('POSTGRES_HOST')

rabbitmq_host = os.environ.get('RABBITMQ_HOST')
rabbitmq = pika.ConnectionParameters(host=rabbitmq_host)


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



class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    username = username = db.Column(db.String(64))
    item_id = db.Column(db.Integer)
    rating_value = db.Column(db.Integer)

    def __repr__(self):
        return '<Rating {}>'.format(self.rating_id)    

db.create_all()



@app.route('/api/v1.0/add_rating', methods=['POST'])
def add_rating():
    data = request.json #{"token": token, "item_id": itemid, "rating_value" 0-10}
    
    if data is None \
        or not 'token' in data \
        or not 'item_id' in data \
        or not 'rating_value' in data:
        return 'Incorrect data', 400
    

    token_json = None

    try:
        token_json = jwt.decode(data['token'], os.environ.get('JWT_SECRET'), algorithms=['HS256'])
    except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError):
        pass

    rating_value = None

    try:
        rating_value = int(data['rating_value'])
    except:
        pass

    if token_json is None or 'username' not in token_json\
        or rating_value is None or rating_value < 1 or rating_value > 10:
        return 'Incorrect data', 400

    username = token_json['username']
    item_id = data['item_id']

    new_rating = Rating(username=username, rating_value = rating_value, item_id = item_id)
    db.session.add(new_rating)
    db.session.commit()

    connection = pika.BlockingConnection(rabbitmq)
    channel = connection.channel()
    channel.queue_declare(queue='update_user', durable=True)
    channel.queue_declare(queue='update_item', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='update_user',
        body=username,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    channel.basic_publish(
        exchange='',
        routing_key='update_item',
        body=item_id,
                properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )
    connection.close()

    return jsonify("Added rating"), 200

@app.route('/api/v1.0/get_user_ratings', methods=['GET'])
def get_user_ratings():
    data = request.json #{"token": token}
    
    if data is None or not 'token' in data:
        return 'Incorrect data', 400
    

    token_json = None

    try:
        token_json = jwt.decode(data['token'], os.environ.get('JWT_SECRET'), algorithms=['HS256'])
    except (jwt.exceptions.InvalidSignatureError, jwt.exceptions.DecodeError):
        pass

    if token_json is None or 'username' not in token_json:
        return 'Incorrect data', 400

    user_ratings = Rating.query.filter_by(username=token_json['username']).all()
    results = [{"item_id": r.item_id, "rating_value": r.rating_value} for r in user_ratings]

    return jsonify(results), 200


@app.route('/api/v1.0/get_item_ratings/<id>', methods=['GET'])
def get_item_ratings(id):

    item_ratings = Rating.query.filter_by(item_id=id).all()

    results = [r.rating_value for r in item_ratings]

    return jsonify(results), 200


@app.route('/identify', methods=['GET'])
def identify():
    return 'Rating service', 200