from flask import Flask
from flask_restful import  Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegistration
from resources.item import Item, Items

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'ahmed'
api = Api(app)

jwt = JWT(app,authenticate, identity) # creates /auth and takes username and password


api.add_resource(Item,'/item/<string:name>')
api.add_resource(Items,'/items')
api.add_resource(UserRegistration,'/register')

if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000,debug=True)