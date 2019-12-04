from flask import Flask, request, Response
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId


app = Flask(__name__)

#Connection avec mongodb

app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/apidb'
mongo = PyMongo(app)


@app.route('/')
def index():
    return "@todo: API documentation"

#Liste tous les utils

@app.route('/api/v1/tools', methods=['GET'])
def list_all_tools():
    tools = mongo.db.tools.find()
    json = dumps(tools)
    return Response(json, mimetype='application/jason')


@app.route('/api/v1/tools/<string:id>', methods=['GET'])
def show_tools(id):
    try:
        tool = mongo.db.tools.find_one({'_id' : ObjectId(id)})
        res = dumps(tool)
        code = 200 if tool else 404
    except:
        code = 404
    finally:
        return Response(res, status=code, mimetype='application/json')


@app.route('/api/v1/tools', methods=['POST'])
def create_tools():
    tool = request.get_json()
    # @todo: verrify 
    mongo.db.tools.insert(tool)
    return Response(dumps(tool), status=201)

@app.route('/api/v1/tools/<string:id>', methods=['PUT'])
def update_tools(id):
    try:
        data = request.get_json()
        mongo.db.tools.find_one_and_update(
            {'_id': ObjectId(id)},
            {'$set' : data}
        )
        code = 204
    except:
        code = 404
    return Response(None, status=code)

@app.route('/api/v1/tools/<string:id>', methods=['DELETE'])
def delete_tools(id):
   try:
       mongo.db.tools.delete_one({'_id' : ObjectId(id)})
       code = 202
   except:
       code = 400
   finally:
       return Reponse(None, status=code)
   
   
# @app.route('/api/v1/tools/<string:id>', methods=['PUT'])
# def update_tools(id):
#     return "@todo: create new tool:" + id

