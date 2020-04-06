import sqlite3
# db
from db import db
from flask_restful import reqparse


class UserModel(db.Model):
    # set up SQLAlchemy
    __tablename__ = 'users'
    
    # show the columns in the model
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        connection = sqlite3.connect('code/data.db')
        cursor = connection.cursor()

        query = '''SELECT * FROM users WHERE username=?'''
        result = cursor.execute(query, (username,)) # parameters must be in the form of a tuple
        row = result.fetchone()
        if row:
            # user = cls(row[0]. row[1], row[2])
            user = cls(*row) # simplifies the above
        else:
            user = None 
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('code/data.db')
        cursor = connection.cursor()

        query = '''SELECT * FROM users WHERE id=?'''
        result = cursor.execute(query, (_id,)) # parameters must be in the form of a tuple
        row = result.fetchone()
        if row:
            # user = cls(row[0]. row[1], row[2])
            user = cls(*row) # simplifies the above
        else:
            user = None 
        connection.close()
        return user