from odoo import models,api,fields,exceptions

class VaultSettings(models.Model):
    _name = "spot_check.vault_setting"
    _inherit="mail.thread"
    _description = "This is an ATM model"
    _rec_name ="branch_id"


    branch_id = fields.Many2one('spot_check.branch',string ='Branch' ,required=True)
    currency_type = fields.Selection([('UGX', 'UGX'),('USD', 'USD')], string="Currency type")
    spot_type = fields.Selection([('Vault', 'Vault'),('ATM', 'ATM'),('MM', 'Mobile Money'),('Teller', 'Teller')], string="Spot Check Type")
    from_date =  fields.Datetime(string='From Date', default=lambda self: fields.datetime.now())
    to_date =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    expected_no =  fields.Integer(string='Expected Number of Spot Checks', default=2)
    actual_no =  fields.Integer(string='Actual Spot Checks')
    spot_check_date =  fields.Datetime(string='Date')

  


