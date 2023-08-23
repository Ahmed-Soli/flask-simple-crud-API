from flask import Flask, jsonify, request


app = Flask(__name__)

stores = [
    {
        'name': 'my wonderful store',
        'items' : [
            {
                'name' : 'my item',
                'price' : 15.99
            }
        ]
    }
]

# POST /store data: {name:}
@app.route('/stores',methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name' : request_data['name'],
        'items' : []
    }
    stores.append(new_store)
    return jsonify(new_store)


# GET /stores/<string:name>
@app.route('/stores/<string:name>',methods=['GET'])
def get_store(name):
    # iterate over stores, if the store name matches, return it, if not return error message
    for store in stores:
        if store['name'] == name:
            return jsonify(store)
    return jsonify({'message':'store not found'})

# /stores GET -> return list of stores
@app.route('/stores')
def get_stores():
    return jsonify({'stores':stores})

# POST /stores/<string:name>/item {name:, price}
@app.route('/stores/<string:name>/item',methods=['POST'])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store['name'] == name:
            new_item = {
                'name' : request_data['name'],
                'price' : request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)

    return jsonify({'message':'store not found'})
    
# GET /stores/<string:name>/item 
@app.route('/stores/<string:name>/item',methods=['GET'])
def get_item_in_store(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items':store['items']})
    return jsonify({'message':'item not found'})


app.run(port=5000)