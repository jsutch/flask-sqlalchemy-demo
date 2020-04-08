from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    """ 
    Class for Store resource
    """
    def get(self, name):
        """
        get store
        """
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        """
        Create a store
        """
        if StoreModel.find_by_name(name):
            return {'message': "A store with name '{}' already exists.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred creating the store."}, 500

        return store.json(), 201

    def delete(self, name):
        """
        Delete a store
        """
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {'message': 'Store deleted'}


class StoreList(Resource):
    """
    Class for StoreList endpoint
    """
    def get(self):
        """
        Return a list of all stores
        """
        return {'stores': list(map(lambda x: x.json(), StoreModel.query.all()))}