from flask import Flask, jsonify
from flask_restful import Api, reqparse
from flask_jwt_extended import JWTManager
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

# db
from db import db
# resources
from resources.apitest import Test
from resources.user import (
    UserRegister,
    User,
    UserList,
    UserLogin,
    UserLogout,
    TokenRefresh
)
from resources.item import Item, ItemList
from resources.store import Store, StoreList

from blacklist import BLACKLIST

# credentials pulled from creds.py
uname = creds.username
passwd = creds.password
fullSqlLitePath = creds.fullSqlLitePath

# instantiate app
app = Flask(__name__)

# configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = fullSqlLitePath
#app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{uname}:{passwd}@localhost/datadb' # using mysql
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #turn off Flask_SQLAlchemy change tracker
app.config['PROPAGATE_EXCEPTIONS'] = True # return internal errors, not just 500, to the user
# db.init_app(app)

# add secret key for auth
app.secret_key = 'hummingbird'
# instantiate API
api = Api(app)

# adding SQLAlchemy datastore creation
@app.before_first_request
def create_tables():
    """
    Create a datastore at SQLALCHEMY_DATABASE_URI and the tables inside,
    unless they exist already
    """
    db.create_all()

# JWT configuration
# app.config['JWT_AUTH_URL_RULE'] = '/login' # login with /login instead of /auth
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1) # 2 hours
# config JWT auth key name to be 'email' instead of default 'username'
# app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
# app.config['JWT_DEFAULT_REALM'] = ''
# app.config['JWT_SECRET_KEY'] = 'bluebird' # different from app.secret key

# JWT Blacklisting
app.config['JWT_BLACKLIST_ENABLED'] = True # enable JWT blacklist
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access','refresh'] # enable for these two actions

# create jwt object
jwt = JWTManager(app) # doesn't create an auth endopint


# @jwt.token_in_blacklist_loader # returns true if the id sent is in the blacklist
# def check_if_token_in_blacklist(decrypted_token):
#     return decrypted_token['identity'] in BLACKLIST 

@jwt.token_in_blacklist_loader # returns true if the token jti sent is in the blacklist
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST 

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1: # instead of hard coding this, should read from a config file/db
        return {'is_admin': True}
    return {'is_admin': False}

@jwt.expired_token_loader
def expired_token_callback():
    """
    Customized error for token expiration
    """
    return jsonify({
        'description': 'The token as expired',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    """
    random string in auth header
    """
    return jsonify({
        'error': 'invalid token',
        'description': 'Signiture validation failed'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    """
    unauthorized endpoint
    """
    return jsonify({
        'error': 'unauthorized endpoint',
        'description': 'unauthorized endpoint'
    }), 401

@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    """
    need a fresh token
    """
    return jsonify({
        'error': 'invalid token',
        'description': 'Need a fresh token'
    }), 401

@jwt.revoked_token_loader
def revoked_token_callback():
    """
    token revoked. add to revoked token list
    """
    return jsonify({
        'error': 'invalid token',
        'description': 'token is no longer valid sucker',
    }), 401

# Adding resources:
# api.add_resource(xxx) replaces @app.route('xxx') under <Class>:get   
# Raw API Tester
# api.add_resource(Test,'/test/<string:name>')

# Item API targets
api.add_resource(Item,'/item/<string:name>') # e.g. http://localhost/item/mittens
api.add_resource(ItemList, '/items')

# User API targets
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(UserRegister,'/register')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserList, '/users')
api.add_resource(TokenRefresh,'/refresh')
# Store API targets
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')


# Debug
if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
# Non-Debug
#if __name__ == '__main__':
    #app.run(port=5000)

# end
