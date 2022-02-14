from odoo import models, fields

class res_userz(models.Model):
    _inherit = 'res.partner'
    
    user_role = fields.Selection([('credit_supervisor', 'Credit Supervisor'),('manager', 'Branch Manager'), ('accountant', 'Branch Accountant'),('cash_center', 'Cash Support Team')], string="User Role",required=True)
    supervisor = fields.Many2one('res.partner',string ='Supervisor')
    branch_ids = fields.Many2one('spot_check.branch',string ='Parent Branch', required=True)


