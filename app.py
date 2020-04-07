from flask import Flask
from flask_restful import Api, reqparse
from flask_jwt import JWT, current_identity
from datetime import timedelta
import os

# exception handling
import werkzeug
from flask_sqlalchemy import get_debug_queries
#from sqlalchemy_debug import sql_debug

# add logging
import logging


# our libraries
import creds

# security
from security import authenticate, identity 
# db
from db import db
# resources
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.apitest import Test

# credentials
uname = creds.username
passwd = creds.password

# instantiate app
app = Flask(__name__)

# configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' 
#app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{uname}:{passwd}@localhost/datadb'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join('code', '/data.db')
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////code/data.db'  #both 3 and 4 ///s fail
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turn off Flask_SQLAlchemy change tracker
# db.init_app(app)

# add secret key for auth
app.secret_key = 'hummingbird'
# instantiate API
api = Api(app)

# JWT configuration
# default creates a new endpoint of /auth
# this can be tailored with app.config
app.config['JWT_AUTH_URL_RULE'] = '/login'
# config JWT to expire within half an hour
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=7200)
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

@app.after_request
def sql_debug(response):
    # logging.basicConfig(filename='code/queries.log',level=logging.DEBUG)
    queries = list(get_debug_queries())
    query_str = ''
    total_duration = 0.0
    for q in queries:
        total_duration += q.duration
        stmt = str(q.statement % q.parameters).replace('\n', '\n       ')
        query_str += 'Query: {0}\nDuration: {1}ms\n\n'.format(stmt, round(q.duration * 1000, 2))

    print('=' * 80)
    print(' SQL Queries - {0} Queries Executed in {1}ms'.format(len(queries), round(total_duration * 1000, 2)))
    print('=' * 80)
    print(query_str.rstrip('\n'))
    print('=' * 80 + '\n')

    # logging.debug(response) 
    return response


# Debug
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
# Non-Debug
#if __name__ == '__main__':
    #app.run(port=5000)




