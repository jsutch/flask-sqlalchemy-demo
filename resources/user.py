from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required
from werkzeug.security import safe_str_cmp

# our imports
from models.user import UserModel
from db import db
from models.user import UserModel

# migrating this out since it's being called by multiple classes
# "_user" turns this into a private variable _user
_user_parser = reqparse.RequestParser() #reqparser can also be used for form fields, also
_user_parser.add_argument('username',
                            type=str,
                            required=True,
                            help='username cannot be left blank'
                            )
_user_parser.add_argument('password',
                            type=str,
                            required=True,
                            help='password cannot be left blank'
                            )


class UserRegister(Resource):
    """
    Register New Users
    """            
    def post(self):
        """
        For /register. Add user to datastore
        """
        data = _user_parser.parse_args()

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
    #@jwt_required
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
    #@jwt_required
    def delete(cls, user_id):
        """
        delete a user by id
        """
        user = UserModel.find_by_id(user_id)
        if user:
            user.delete_from_db()
        return {'message':'User {} Deleted'.format(user.username    )}


class UserList(Resource):
    @jwt_required
    def get(self):
        """
        Get a list of users and return in json form
        """
        return {'users': [x.json() for x in UserModel.find_all()]}

class UserLogin(Resource):
    """
    Create User Login functions
    """
    @classmethod
    def post(cls):
        """
        Authenticate a user, create access and refresh tokens and return them to user
        This does what the 'authenticate' function did in earlier code
        """
        data = _user_parser.parse_args()
        user = UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password, data['password']):
            # 'identity=' is what identity() did in old code
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200
        return {'message':'Invalid credentials'}, 401



