from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.user import UserModel

from db import db
#from models.item import find_by_name, insert, update
from models.user import UserModel

class UserRegister(Resource):
    # Move parser within user
    parser = reqparse.RequestParser() #reqparser can also be used for form fields, also
    parser.add_argument('username',
        type=str,
        required=True,
        help='username cannot be left blank'
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help='password cannot be left blank'
    )
            
    def post(self):
        """
        For /register. Add user to datastore
        """
        data = UserRegister.parser.parse_args()

        # Call find_by_name
        if UserModel.find_by_username(data['username']):
            return {'message': "An user with name '{}' already exists".format(data['username'])}, 404

        user = UserModel(**data)

        try:
            user.save_to_db()
        except:
            return {'message':'Save to db failed'}, 500

        return {"message": "User created successfully."}, 201

class User(Resource):
    @classmethod
    #@jwt_required() 
    def get(cls, user_id):
        """
        get user by id
        """
        user = UserModel.find_by_id(user_id)
        if not user:
            return {'message': 'User {} not found'.format(user)}, 404
        else:
            return user.json()

    @classmethod
    #@jwt_required() 
    def delete(cls, user_id):
        """
        delete a user by id
        """
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
        return {'message':'User {} Deleted'.format(user.username    )}


class UserList(Resource):
    @jwt_required()
    def get(self):
        """
        Get a list of users and return in json form
        """
        return {'users': [x.json() for x in UserModel.find_all()]}