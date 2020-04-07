from db import db

# logging config
import logging
logging.basicConfig(filename='code/testing.log',level=logging.DEBUG)

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
        An internal method to do database lookups.
        SQLAlchemy method
        """
        # examples
        #return ItemModel.query.fiter_by(name=name).filter_by(id=1) # select * from items where name=name and id=1
        #return ItemModel.query.fiter_by(name=name, id=1)# another method. Returns itemmodel object
        try:
            logging.debug(name, cls.query.filter_by(name=name).first())
            return cls.query.filter_by(name=name).first() # select * from items where name=name, limit 1
        except Exception as e:
            logging.debug('Exception:',e)
            return e

    def save_to_db(self):
        """
        insert item into datastore. 
        SQLAlchemy method combines insert and update methods ("upserting")
        """
        try:
            print("saving to db called", self)
            db.session.add(self)
        except Exception as e:
            return e
        db.commit()

    def delete_from_db(self):
        """
        Delete object from datastore
        """
        db.session.delete(self)
        db.commit()