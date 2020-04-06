import sqlite3
# db
from db import db

class ItemModel(db.Model):
    """
    ItemModel Class
    internal methods that don't interact with Flask API
    """
    __tablename__ = 'items'
    
    # show the columns in the model
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    
    def __init__(self, name, price):
        self.name = name
        self.price = price
    def json(self):
        return {'name':self.name,'price':self.price}

    @classmethod
    def find_by_name(cls, name):
        """
        An internal method to do database lookups
        """
        connection = sqlite3.connect('code/data.db')
        cursor = connection.cursor()

        query = '''SELECT * FROM items WHERE name =?'''
        result = cursor.execute(query, (name, ))
        row = result.fetchone()
        connection.close()

        if row:
            # update the return of the objects to use classmethod methods
            #return cls(row[0], row[1]) #using positional arguments from the class init - cls(name, price) == ItemModel(row[0],row[1])
            # since this changes the output from a dict, resources.item.py must use the item.json()
            # for the correct format
            return cls(*row) #using tuple unpacking. same return

    def insert(self):
        """
        insert item into datastore
        """
        connection = sqlite3.connect('code/data.db')
        cursor = connection.cursor()

        query = '''INSERT INTO items VALUES (?,?)'''
        cursor.execute(query, (self.name, self.price))

        connection.commit()
        connection.close()

    def update(self):
        """
        Update an item in the datastore
        """
        connection = sqlite3.connect('code/data.db')
        cursor = connection.cursor()

        query = '''UPDATE items SET price=? WHERE name=?'''
        cursor.execute(query, (self.price, self.name))

        connection.commit()
        connection.close()