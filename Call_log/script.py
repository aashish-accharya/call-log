from xmlrpc import client as xmlrpclib

url = 'http://192.168.2.123:8069'
db = 'odoo'
username = 'admin'
password = 'admin'

common = xmlrpclib.ServerProxy('{}/xmlrpc/2/common'.format(url))
uid = common.authenticate(db, username, password, {})

models = xmlrpclib.ServerProxy('{}/xmlrpc/2/object'.format(url))
# models.execute_kw(db, uid, password,
#     'call.log', 'create',
#     [{
#         'called_from': 1,
#         'called_to': '12345',
#         'call_type': 'incoming',
#         'call_site': 2,
#         'call_date': '2022-01-01 00:00:00',
#         'call_duration': 60,
#         'call_remarks': 'Test',
#     }])
