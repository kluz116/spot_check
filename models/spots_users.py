from odoo import models, fields

class res_user(models.Model):
    _inherit = 'res.partner'
    
    user_role = fields.Selection([('credit_supervisor', 'Credit Supervisor'),('manager', 'Branch Manager'), ('accountant', 'Branch Accountant'),('cash_center', 'Cash Support Team')], string="User Role",required=True)
    supervises = fields.Many2one('res.partner',string ='Supervises')
    #branch_id = fields.Many2one('spot_check.branch',string ='Parent Branch', required=True)


