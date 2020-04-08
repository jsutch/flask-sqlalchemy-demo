from flask_restful import Resource, reqparse
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

        user = UserModel(data['username'], data['password'])

        try:
            user.save_to_db()
        except:
            return {'message':'Save to db failed'}, 500

        return {"message": "User created successfully."}, 201
