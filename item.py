import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help='This field can not be left blank!')

    @jwt_required()
    def get(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()
        
        if row:
            return {'item' : {'name':row[0], 'price':row[1]}}
        return {'message': 'Item not found'}, 404
    
    def post(self,name):
        if next(filter(lambda element : element['name'] == name , items),None) :
            return {'message' : 'an item with name {} already exists'.format(name)} , 400
        request_data = Item.parser.parse_args()
        item = {'name':name, 'price':request_data['price']}
        items.append(item)
        return item , 201
    
    def delete(self,name):
        global items
        items = list(filter(lambda elem: elem['name'] != name, items))
        return {'message': f'Item {name} Deleted'}

    def put(self,name):        
        item = next(filter(lambda element : element['name'] == name , items),None)
        request_data = Item.parser.parse_args()
        if item is None: # Create new item
            item = {'name' : name, 'price' : request_data['price']}
            items.append(item)
        else: # Update the item
            item.update(request_data)
        return item

    
class Items(Resource):
    def get(self):
        return {'items' : items}