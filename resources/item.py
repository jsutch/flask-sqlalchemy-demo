import sqlite3
from flask import Flask, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_claims, jwt_optional, get_jwt_identity
# db
from db import db
#from models.item import find_by_name, insert, update
from models.item import ItemModel


class Item(Resource):
    """
    Item Class
    Only for Resources that interact with Flask RESTful
    """
    TABLE_NAME = 'items'
    # parser
    parser = reqparse.RequestParser() #reqparser can also be used for form fields, also
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank'
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help='Every item needs a store association'
    )

    # with flask_jwt_extended, jwt_required no longer takes arguments, so it doesn't need the ()
    @jwt_required
    def get(self, name):
        """
        Accept external requests for items
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}, 404

    @jwt_required
    def post(self, name):
        """
        Add a new item into the database
        """
        # Call find_by_name
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 404

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message':'Save to db failed'}, 500

        return item.json(), 201

    @jwt_required
    def put(self, name):
        """
        Itempotent. Can create or update an item.
        """
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
            item.store_id = data['store_id']
        
        item.save_to_db()

        return item.json()

    @jwt_required 
    def delete(self, name):
        """
        Overwrite items list with a new list that has had 'name' removed
        """
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {'message':'Admin is required'}, 401

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item {} Deleted'.format(name)}


class ItemList(Resource):
    @jwt_optional
    def get(self):
        """
        If user_id is included (logged in), return a full list of items.
        if not, return only a list of item names
        """
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]
        if user_id:
            return {'items': items}, 200
        return {'items':  [item['name'] for item in items],
                'message': 'More data available if you log in'
        }, 200
        
