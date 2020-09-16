curl -XPOST -H "Content-type: application/json" -d '{"username":"user1", "password":"password1"}' '127.0.0.1:85/api/v1.0/create_user'

curl -XPOST -H "Content-type: application/json" -d '{"username":"user1", "password":"password1"}' '127.0.0.1:85/api/v1.0/get_token'


curl -XPOST -H "Content-type: application/json" -d '{"name":"Great Item", "description":"This item is great"}' '127.0.0.1:81/api/v1.0/add_item'
curl -XPOST -H "Content-type: application/json" -d '{"name":"Great Item2", "description":"This item is better"}' '127.0.0.1:81/api/v1.0/add_item'

curl '127.0.0.1:81/api/v1.0/get_item_data/1'


curl -XPOST -H "Content-type: application/json" -d '{"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIxIn0.1V0RKjiZwFK5DMN3U34VgIsNg4VMMjP6vsyL7RGdchc", "item_id":"1", "rating_value": 10}' '127.0.0.1:82/api/v1.0/add_rating'

curl -X GET -H "Content-type: application/json" -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIxIn0.1V0RKjiZwFK5DMN3U34VgIsNg4VMMjP6vsyL7RGdchc"}' '127.0.0.1:82/api/v1.0/get_user_ratings'

curl '127.0.0.1:82/api/v1.0/get_item_ratings/1'

curl -X GET -H "Content-type: application/json" -d '{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIxIn0.1V0RKjiZwFK5DMN3U34VgIsNg4VMMjP6vsyL7RGdchc"}' '127.0.0.1:83/api/v1.0/get_user_recommendations'

curl '127.0.0.1:83/api/v1.0/get_item_recommendations/1'
