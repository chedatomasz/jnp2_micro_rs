curl -XPOST -H "Content-type: application/json" -d '{"username":"user1", "password":"password1"}' '127.0.0.1:5000/api/v1.0/create_user'

curl -XPOST -H "Content-type: application/json" -d '{"username":"user1", "password":"password1"}' '127.0.0.1:5000/api/v1.0/get_token'
