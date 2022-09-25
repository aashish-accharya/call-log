from flask import Flask,jsonify
from flask_restful import Resource, Api
from xmlrpc import client as xmlrpclib
import json

app = Flask(__name__)
api = Api(app)

url = 'http://192.168.2.123:8069'
db = 'odoo'
username = 'admin'
password = 'admin'

# data = {'called_from': 1,
#         'called_to': '12345',
#         'call_type': 'incoming',
#         'call_site': 2,
#         'call_date': '2022-01-01 00:00:00',
#         'call_duration': 60,
#         'call_remarks': 'Test',
#     }

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})
models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))

@app.route('/create/<file>', methods=['POST'])
def create(file):
    with open (file) as f:
        data = json.load(f)
    models.execute_kw(db, uid, password,'call.log', 'create',data)
    return jsonify(data)

@app.route('/search/<field>,<value>')
def search(field, value):
    yo = models.execute_kw(db, uid, password,"call.log", "search_read", [[[field, "=", value]]])
    return jsonify(yo)

@app.route('/delete/<value>')
def delete(value):
    data = models.execute_kw(db, uid, password,'call.log', 'unlink', [value])
    return jsonify(data)

@app.route('/get')
def get():
    data = models.execute_kw(db, uid, password,'call.log', 'fields_get', [["called_from", "called_to", "call_type", "call_site", "call_date", "call_duration", "call_remarks"]])
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)