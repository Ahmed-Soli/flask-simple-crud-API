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
            item.save_to_db()
        except :
            return {'message': 'Error occured while inserting'} , 500
              
        return item.json() , 201  

    def delete(self,name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()
            return {'message': f'Item {name} Deleted'}
        return {'message': f'Item {name} Not Found'} , 400
                

    def put(self,name):        
        request_data = Item.parser.parse_args()
        item = ItemModel.find_item_by_name(name)
        if item is None: # Create new item
            item = ItemModel(name, request_data['price'])
        else: # Update the item
            item.price = request_data['price']
        item.save_to_db()
        return item.json()
    

class Items(Resource):
    def get(self):
        return {'items' : [item.json() for item in ItemModel.query.all()]}