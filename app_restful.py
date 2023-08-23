from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'ahmed'
api = Api(app)

jwt = JWT(app,authenticate, identity) # creates /auth and takes username and password

items = []
class Item(Resource):
    @jwt_required()
    def get(self,name):
        item = next(filter(lambda element : element['name'] == name , items),None)
        return {'item':item} , 200 if item else 404
    
    def post(self,name):
        if next(filter(lambda element : element['name'] == name , items),None) :
            return {'message' : 'an item with name {} already exists'.format(name)} , 400
        request_data = request.get_json()
        item = {'name':name, 'price':request_data['price']}
        items.append(item)
        return item , 201
    
    def delete(self,name):
        global items
        items = list(filter(lambda elem: elem['name'] != name, items))
        return {'message': f'Item {name} Deleted'}

    def put(self,name):
        item = next(filter(lambda element : element['name'] == name , items),None)
        request_data = request.get_json()
        if item is None: # Create new item
            item = {'name' : name, 'price' : request_data['price']}
            items.append(item)
        else: # Update the item
            item.update(request_data)
        return item

    
class Items(Resource):
    def get(self):
        return {'items' : items}
    

api.add_resource(Item,'/item/<string:name>')
api.add_resource(Items,'/items')
app.run(port=5000,debug=True)