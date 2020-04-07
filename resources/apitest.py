#from flask_restful import Resource
from flask import Flask, request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
# db
from db import db
#from models.item import find_by_name, insert, update
from models.item import ItemModel

class Test(Resource):
    """
    test harness. return whatever name passed
    """
    # def get(self, name):
    #     """
    #     Raw returns 
    #     """
    #     return {'test':name}
    
    def get(self, name):
        """
        testing models.Item.ItemModel
        """
        return {'type': type(ItemModel.find_by_name(name))}