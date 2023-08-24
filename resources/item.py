import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help='This field can not be left blank!')

    @jwt_required()
    def get(self,name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404
    
    def post(self,name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return {'message' : 'an item with name {} already exists'.format(name)} , 400
        request_data = Item.parser.parse_args()
        item = ItemModel(name, request_data['price'])
        try:
            item.insert(item)
        except :
            return {'message': 'Error occured while inserting'} , 500
              
        return item , 201  

    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))
        connection.commit()
        connection.close()
                
        return {'message': f'Item {name} Deleted'}

    def put(self,name):        
        request_data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)
        updated_item = ItemModel(name, request_data['price'])
        if item is None: # Create new item
            try:
                updated_item.insert()
            except :
                return {'message': 'Error occured while inserting'} , 500
        else: # Update the item
            try:
                updated_item.update()
            except :
                return {'message': 'Error occured while inserting'} , 500
        return updated_item.json()
    

class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * from items"
        result = cursor.execute(query)
        items = []
        for item in result:
            items.append({'name':item[0],'price':item[1]})
        connection.commit()
        connection.close()
    
        return {'items' : items}