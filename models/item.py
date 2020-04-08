from db import db

# logging config
import logging
logging.basicConfig(filename='code/testing.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
# logging.basicConfig(format='%(asctime)s %(message)s')

class ItemModel(db.Model):
    """
    ItemModel Class
    internal methods that don't interact with Flask API
    """
    __tablename__ = 'items'
    
    # show the columns in the model
    # SQLAlchemy can use these definitions to create a new datastore at start.
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    # adding a new column for store id
    store_id = db.Column(db.Integer, db.ForeignKey('stores.id'))
    store = db.relationship('StoreModel') # obviates need for joins
    
    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name':self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        """
        An internal method to do database lookups.
        SQLAlchemy method
        """
        # examples
        #return ItemModel.query.fiter_by(name=name).filter_by(id=1) # select * from items where name=name and id=1
        #return ItemModel.query.fiter_by(name=name, id=1)# another method. Returns itemmodel object
        try:
            # logging.debug('find_by_name() called: ', name, cls.query.filter_by(name=name).first())
            return cls.query.filter_by(name=name).first() # select * from items where name=name, limit 1
        except Exception as e:  
            logging.debug('Exception:', e)
            return e

    def save_to_db(self):
        """
        insert item into datastore. 
        SQLAlchemy method combines insert and update methods ("upserting")
        """
        db.session.add(self)
        try:
            #logging.debug("save_to_db.commit()")
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