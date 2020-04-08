from db import db

# logging config
import logging
logging.basicConfig(filename='code/testing.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
# logging.basicConfig(format='%(asctime)s %(message)s')

class StoreModel(db.Model):
    """
    StoreModel Class
    internal methods that don't interact with Flask API
    """
    __tablename__ = 'stores'
    
    # show the columns in the model
    # SQLAlchemy can use these definitions to create a new datastore at start.
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    # create backreference for items
    #items = db.relationship('ItemModel')
    # lazy flag: don't automatically go into items and create an object for each item
    # this makes the table creation faster
    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        """
        Goes into items table every time this is called. Makes this call slower.
        """
        return {'name':self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def find_by_name(cls, name):
        """
        Find element by name
        """
        try:
            return cls.query.filter_by(name=name).first() # select * from items where name=name, limit 1
        except Exception as e:  
            logging.debug('Exception:', e)
            return e

    def save_to_db(self):
        """
        insert item into datastore.
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
