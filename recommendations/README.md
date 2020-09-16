curl -X GET -H "Content-type: application/json" -d '{"token": token}' '127.0.0.1:5000/api/v1.0/get_user_recommendations'

curl '127.0.0.1:5000/api/v1.0/get_item_recommendations/REPLACEME/'
