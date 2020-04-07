import sqlite3
from flask import Flask, request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
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

    @jwt_required()
    def get(self, name):
        """
        Accept external requests for items
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message':'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        """
        Add a new item into the database
        """
        # Call find_by_name
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 404

        data = Item.parser.parse_args()
        # change item to be an ItemModel object, not a dict
        # item = {'name':name,'price': data['price']}
        item = ItemModel(name, data['price'])
        try:
            item.save_to_db()
        except:
            return {'message':'Save to db failed'}, 500

        return item.json(), 201

    @jwt_required()
    def put(self, name):
        """
        Itempotent. Can create or update an item.
        """
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name,data['price'])
        else:
            item.price = data['price']
        
        item.save_to_db()

        return updated_item.json()

    @jwt_required()   
    def delete(self, name):
        """
        Overwrite items list with a new list that has had 'name' removed
        """
        item = Item.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'Item Deleted'}


class ItemList(Resource):
    @jwt_required()
    def get(self):
        """
        Return a list of all items
        """
        connection = sqlite3.connect('code/data.db')
        cursor = connection.cursor()

        query = '''SELECT * FROM items'''
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name':row[0], 'price':row[1]})
        
        connection.close()

        return {'items': items }, 200
