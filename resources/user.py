import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):
    # Move parser within item instead of function by function
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
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message':'Username already exists'}, 404
        # create user
        connection = sqlite3.connect('code/data.db')
        cursor = connection.cursor()

        query = '''INSERT INTO users VALUES(NULL, ?, ?)'''
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()
        
        return {'message':'User created successfully'}, 201
            

