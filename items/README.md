curl -XPOST -H "Content-type: application/json" -d '{"name":"Great Item", "description":"This item is great"}' '127.0.0.1:5000/api/v1.0/add_item'

curl '127.0.0.1:5000/api/v1.0/get_item_data/REPLACEME/'
