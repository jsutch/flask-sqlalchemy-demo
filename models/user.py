import sqlite3
# db
from db import db
from flask_restful import reqparse
# logging config
import logging
logging.basicConfig(filename='code/testing.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class UserModel(db.Model):
    """
     Internal calls that don't interact with users
    """
    # set up SQLAlchemy
    __tablename__ = 'users'
    
    # show the columns in the model
    # SQLAlchemy can use these definitions to create a new datastore at start.
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        """
        lookup for users in the users table
        """
        try:
            return cls.query.filter_by(username=username).first()
        except Exception as e:  
            logging.debug('Exception:', e)
            return e

    @classmethod
    def find_by_id(cls, _id):
        """
        lookup for ids in the users table
        """
        try:
            return cls.query.filter_by(id=_id).first()
        except Exception as e:  
            logging.debug('Exception:', e)
            return e

    def save_to_db(self):
        """
        insert user into datastore.
        """
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            logging.debug('save_to_db.commit() Exception: ', e)
            return e

    def delete_from_db(self):
        """
        Delete object from datastore
        """
        db.session.delete(self)
        db.session.commit()