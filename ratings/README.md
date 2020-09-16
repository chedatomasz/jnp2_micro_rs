curl -XPOST -H "Content-type: application/json" -d '{"token":"user1", "item_id":"1", "rating_value": 10}' '127.0.0.1:5000/api/v1.0/add_rating'

curl -X GET -H "Content-type: application/json" -d '{"token": token}' '127.0.0.1:5000/api/v1.0/get_user_ratings'

curl '127.0.0.1:5000/api/v1.0/get_item_ratings/REPLACEME/'
