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
#setting credentials

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

def getUid():
    """Get the uid of the user from odoo server"""
    uid = common.authenticate(db, getUsername(), getPassword(), {})
    if not uid:
        raise Exception('Authentication failed')
    return uid

def getUsername():
    """Username of user from request header"""
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
    """Create record on Odoo Server
    Place json data in request body
    return json data of created record
    """
    try:
        data = request.get_json()
        password = getPassword()
        uid = getUid()
        models.execute_kw(db, uid, password,'call.log', 'create',data)
        return jsonify(data)
    except Exception as e:
        return jsonify({'Error':str(e)})

@app.route('/search/<field>,<value>')
def search(field, value):
    """Search record on Odoo Server
    search by using the field name and value for respective field
    return json data of searched record
    """
    try:
        password = getPassword()
        uid = getUid()
        data = models.execute_kw(db, uid, password,"call.log", "search_read", [[[field, "=", value]]])
        if len(data) == 0:
            raise Exception('Requested data not found')
        else:
            return jsonify(data)
    except Exception as e:
        return jsonify({'Error':str(e)})

@app.route('/delete/<value>', methods=['DELETE'])
def delete(value):
    """Delete Call Log record using record ID"""
    try:
        password = getPassword()
        uid = getUid()
        data = models.execute_kw(db, uid, password,'call.log', 'unlink', [value])
        return jsonify(data)
    except Exception as e:
        return jsonify({'Error':str(e)})

@app.route('/get')
def get():
    """Get all fields in Call Log module"""
    try:
        password = getPassword()
        uid = getUid()
        data = models.execute_kw(db, uid, password,'call.log', 'fields_get', [[]])
        print(len(data))
        if len(data) == 0:
            raise Exception('No data found')
        else:
            return jsonify(data)
    except Exception as e:
        return jsonify({'Error':str(e)})

@app.route('/update/<int:id>', methods=['PUT'])
def update(id):
    """Update Call Log record using record ID
    Place updated json data in request body
    """
    data = request.get_json()
    password = getPassword()
    uid = getUid()
    models.execute_kw(db, uid, password,'call.log', 'write', [[id], data])
    return jsonify(data)

@app.route('/authorize/<uname>,<passw>')
def authorize(uname, passw):
    """Authorize user"""
    uid = common.authenticate(db, uname, passw, {})
    if not uid:
        return jsonify({'status': 'failed'})
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

