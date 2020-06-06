from flask import Flask,request
from flask_restful import Api , Resource
from flask_jwt import JWT ,jwt_required , current_identity
from security import authenticate , identity

app = Flask(__name__)
app.secret_key = "sangam"
api = Api(app)
jwt = JWT(app, authenticate, identity)

items = []


@app.route("/protected")
@jwt_required()
def protected():
    return f"{current_identity}"


class Item(Resource):
    @jwt_required()
    def get(self,nam=None):
        item = next(filter(lambda x:x['name'] == nam, items), None)
        return {'item':item} ,200 if item else 404

    @jwt_required()
    def post(self,nam=None):
        if next(filter(lambda x:x['name'] == nam,items),None):
            return{'message':"an item with name '{}' already exist." .format(nam)}
        data = request.get_json()
        item = {'name':nam,
        'price':data['price']}
        items.append(item)
        return item,201

    @jwt_required()
    def delete(self,nam=None):
        global items
        items = list(filter(lambda x:x['name'] != nam,items))
        return{'message':'item deleted'}

    @jwt_required()
    def put(self,nam=None):
        data = request.get_json()
        item = next(filter(lambda x:x['name'] == nam,items),None)
        if item is None:
            item = {'name':nam,'price':data['price']}
            items.append(item)
        else:
            item.update(data)
        return item

class item_list(Resource):
    @jwt_required()
    def get(self):
        return {'items':items}

api.add_resource(Item,'/item/<nam>')
api.add_resource(item_list,'/items')
app.run(port = 5000 , debug = True)
