from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3
from TestSQLALCHEMY.models.store import StoreModel


class Store(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Item not found'}, 404



    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}

        return store.json(),201



    @jwt_required()
    def put(self, name):
        data = Store.parser.parse_args()
        item = StoreModel.find_by_name(name)
        if item is None:
            item = StoreModel(name)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
        return {'message': 'Item deleted'}


class StoreList(Resource):
    def get(self):
        return {"Stores" : [store.json() for store in StoreModel.query.all()]}
        # return {"Items" : list(map(lambda x : x.json(), ItemModel.query.all()))}