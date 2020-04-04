import sqlite3
from flask import Flask, request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
#from models.item import find_by_name, insert, update
from models.item import ItemModel

class Item(Resource):
    """
    Main Item Class
    Flask-RESTful does not need jsonify for returns
    """
    TABLE_NAME = 'items'
    # parser
    parser = reqparse.RequestParser() #reqparser can also be used for form fields, also
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank'
    )

    #@jwt_required()
    def get(self, name):
        """
        Accept external requests for items
        """
        item = ItemModel.find_by_name(name)
        if item:
            return item
        return {'message':'Item not found'}, 404

    #@jwt_required()
    def post(self, name):
        """
        Add a new item into the database
        """
        # if self.find_by_name(name): # two ways to call
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists".format(name)}, 404

        data = Item.parser.parse_args()
        item = {'name':name,'price': data['price']}
        try:
            ItemModel.insert(item)
        except:
            return {'message':'An error occurred'}, 500

        return item, 201

    #@jwt_required()   
    def delete(self, name):
        """
        Overwrite items list with a new list that has had 'name' removed
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = '''DELETE FROM items WHERE name =?'''
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message':'Item Deleted'}

    #@jwt_required()
    def put(self, name):
        """
        Itempotent. Can create or update an item.
        """
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        updated_item = {'name':name,'price': data['price']}

        if item is None:
            try:
                ItemModel.insert(updated_item)
            except:
                return {'message':'An error occurred adding the item'}, 500    
        else:
            try:
                ItemModel.update(updated_item)
            except:
                return {'message':'An error occurred updating the item'}, 500 
        return updated_item 


class ItemList(Resource):
    #@jwt_required()
    def get(self):
        """
        Return a list of all items
        """
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = '''SELECT * FROM items'''
        result = cursor.execute(query)

        items = []
        for row in result:
            items.append({'name':row[0], 'price':row[1]})
        
        connection.close()

        return {'items': items }, 200
