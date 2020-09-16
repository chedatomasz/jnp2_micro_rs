from flask import Flask, request, jsonify
import jwt
import os
import time
import requests

app = Flask(__name__)

@app.route('/api/v1.0/get_user_recommendations', methods=['GET'])
def get_user_recommendations():
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

    user_ratings = requests.get('http://ratings/api/v1.0/get_user_ratings', json = {"token": data["token"]}).json()
    user_ratings.sort(reverse=True, key= lambda x: x['rating_value'])

    results = [x['item_id'] for x in user_ratings[:5]]

    return jsonify(results), 200


@app.route('/api/v1.0/get_item_recommendations/<id>', methods=['GET'])
def get_item_recommendations(id):
    r = requests.get('http://items/api/v1.0/all_items')
    print(r)
    all_items = r.json()
    all_ratings = [requests.get(f'http://ratings/api/v1.0/get_item_ratings/{item_id}').json() for item_id in all_items]

    our_ratings = requests.get(f'http://ratings/api/v1.0/get_item_ratings/{id}').json()

    our_total = sum(our_ratings)

    all_totals = [sum(rs) for rs in all_ratings]

    differences = [abs(their-our_total) for their in all_totals]

    id_diff = [(item_id, diff) for item_id, diff in zip(all_items, differences)]

    id_diff.sort(key=lambda x: x[1])

    results = [x[0] for x in id_diff[:5]]

    return jsonify(results), 200


@app.route('/identify', methods=['GET'])
def identify():
    return 'Recomendation service', 200