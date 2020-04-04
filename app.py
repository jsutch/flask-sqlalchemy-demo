from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT, current_identity
from datetime import timedelta

# our libraries
from security import authenticate, identity 
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.apitest import Test


# instantiate app
app = Flask(__name__)
# add secret key for auth
app.secret_key = 'hummingbird'
# instantiate API
api = Api(app)

# JWT configuration
# default creates a new endpoint of /auth
# this can be tailored with app.config
app.config['JWT_AUTH_URL_RULE'] = '/login'
# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)
# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

# create jwt object
jwt = JWT(app, authenticate, identity)

# Adding resources:
# api.add_resource(xxx) replaces @app.route('xxx') under <Class>:get   
# Raw API Tester
api.add_resource(Test,'/test/<string:name>') 
# Application API targets
api.add_resource(Item,'/item/<string:name>') # e.g. http://localhost/item/mittens
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister,'/register')

# Debug
if __name__ == '__main__':
    app.run(port=5000, debug=True)
# Regular
#if __name__ == '__main__':
    #app.run(port=5000)




