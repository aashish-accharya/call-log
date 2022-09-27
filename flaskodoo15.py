from flask import Flask,jsonify, request
from flask_restful import Api
from xmlrpc import client as xmlrpclib
import base64

app = Flask(__name__)
api = Api(app)

url = 'http://192.168.2.74:8069'
db = 'nyaya'
username=''
password=''


common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

def getUid():
    uid = common.authenticate(db, getUsername(), getPassword(), {})
    if not uid:
        raise Exception('Authentication failed')
    return uid

def getUsername():
    header = request.headers.get('Authorization')
    user=base64.b64decode(header.split(' ')[1])
    username=user.decode('utf-8').split(':')[0]
    return username

def getPassword():
    header = request.headers.get('Authorization')
    user=base64.b64decode(header.split(' ')[1])
    password=user.decode('utf-8').split(':')[1]
    return password

@app.route('/create', methods=['POST'])
def create():
    data = request.get_json()
    password = getPassword()
    uid = getUid()
    models.execute_kw(db, uid, password,'call.log', 'create',data)
    return jsonify(data)

@app.route('/search/<field>,<value>')
def search(field, value):
    password = getPassword()
    uid = getUid()
    yo = models.execute_kw(db, uid, password,"call.log", "search_read", [[[field, "=", value]]])
    return jsonify(yo)

@app.route('/delete/<value>', methods=['DELETE'])
def delete(value):
    password = getPassword()
    uid = getUid()
    data = models.execute_kw(db, uid, password,'call.log', 'unlink', [value])
    return jsonify(data)

@app.route('/get')
def get():
    password = getPassword()
    uid = getUid()
    data = models.execute_kw(db, uid, password,'call.log', 'fields_get', [[]])
    return jsonify(data)

@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    data = request.get_json()
    password = getPassword()
    uid = getUid()
    models.execute_kw(db, uid, password,'call.log', 'write', [[id], data])
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

