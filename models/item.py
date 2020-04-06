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
        An internal method to do database lookups.
        SQLAlchemy method
        """
        # examples
        #return ItemModel.query.fiter_by(name=name).filter_by(id=1) # select * from items where name=name and id=1
        #return ItemModel.query.fiter_by(name=name, id=1)# another method. Returns itemmodel object
        return cls.query.fiter_by(name=name).first() # select * from items where name=name, limit 1

    def save_to_db(self):
        """
        insert item into datastore. 
        SQLAlchemy method combines insert and update methods ("upserting")
        """
        db.session.add(self)
        db.commit()

    def delete_from_db(self):
        """
        Delete object from datastore
        """
        db.session.delete(self)
        db.commit()