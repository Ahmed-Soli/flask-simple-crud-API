import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type=float,required=True,help='This field can not be left blank!')

    @jwt_required()
    def get(self,name):
        item = Item.find_item_by_name(name)
        if item:
            return item
        return {'message': 'Item not found'}, 404
    
    @classmethod
    def find_item_by_name(cls,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items WHERE name=?"
        result = cursor.execute(query,(name,))
        row = result.fetchone()
        connection.close()
        
        if row:
            return {'item' : {'name':row[0], 'price':row[1]}}

    def post(self,name):
        item = Item.find_item_by_name(name)
        if item:
            return {'message' : 'an item with name {} already exists'.format(name)} , 400
        request_data = Item.parser.parse_args()
        item = {'name':name, 'price':request_data['price']}
        try:
            self.insert(item)
        except :
            return {'message': 'Error occured while inserting'} , 500
              
        return item , 201
    
    @classmethod
    def insert(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO items VALUES (?, ?)"
        cursor.execute(query,(item['name'],item['price']))
        connection.commit()
        connection.close()

    def delete(self,name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query,(name,))
        connection.commit()
        connection.close()
                
        return {'message': f'Item {name} Deleted'}

    def put(self,name):        
        item = Item.find_item_by_name(name)
        request_data = Item.parser.parse_args()
        updated_item = {'name' : name, 'price' : request_data['price']}
        if item is None: # Create new item
            try:
                self.insert(updated_item)
            except :
                return {'message': 'Error occured while inserting'} , 500
        else: # Update the item
            try:
                self.update(updated_item)
            except :
                return {'message': 'Error occured while inserting'} , 500
        return updated_item
    
    @classmethod
    def update(cls,item):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(query,(item['price'],item['name']))
        connection.commit()
        connection.close()
    
class Items(Resource):
    def get(self):
        return {'items' : items}