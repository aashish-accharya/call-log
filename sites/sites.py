from odoo import models, fields

class CallLog(models.Model):
    _name='site.info'
    _description='Site Information'
    name=fields.Char('Site Name')
    site_contact=fields.Char('Contact')
    site_address=fields.Char('Address')
    site_person=fields.Char('Person')