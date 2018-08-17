from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from TestSQLALCHEMY.security import authenticate, identity
from TestSQLALCHEMY.resources.user import UserRegister
from TestSQLALCHEMY.resources.item import Item, ItemList
from TestSQLALCHEMY.resources.store import Store,StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
app.config['PROPAGATE_EXCEPTIONS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = 'jose'
api = Api(app)


jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList,'/stores')

if __name__ == '__main__':
    from TestSQLALCHEMY.db import db
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True
