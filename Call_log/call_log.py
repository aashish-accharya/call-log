from odoo import models, fields

class CallLog(models.Model):
    _name='call.log'
    _description='call.log'
    called_from = fields.Many2one('res.users', string='Called From')
    called_to = fields.Char('Called to', required=True)
    call_type = fields.Selection([('incoming', 'Incoming'), ('outgoing', 'Outgoing'), ('missed', 'Missed Call')], 'Call type', required=True)
    call_site = fields.Many2one('site.info', string='Call Site')
    call_date = fields.Datetime('Call date', required=True)
    call_duration = fields.Integer('Call duration', required=True)
    call_remarks = fields.Text('Call remarks')