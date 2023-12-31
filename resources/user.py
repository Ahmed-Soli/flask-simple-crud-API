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
        
        user = UserModel(**request_data)
        user.save_to_db()
        
        return {"message": "User Created Successfully."} , 201

        
