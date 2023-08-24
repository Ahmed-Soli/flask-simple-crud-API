
import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegistration(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    
    def post(self):
        request_data = UserRegistration.parser.parse_args()
        if UserModel.find_by_username(request_data['username']):
            return {"message": "User Already Exists!"} , 400
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query,(request_data['username'], request_data['password']))

        connection.commit()
        connection.close()
        return {"message": "User Created Successfully."} , 201

        
