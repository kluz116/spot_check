from odoo import models, fields

class res_user(models.Model):
    _inherit = 'res.partner'
    
    user_role = fields.Selection([('credit_supervisor', 'Credit Supervisor'),('manager', 'Branch Manager'), ('accountant', 'Branch Accountant'),('cash_center', 'Cash Support Team'),('teller', 'Teller')], string="User Role")
    supervises = fields.Many2one('res.partner',string ='Supervises')
    till_id = fields.Selection(string='Till ID: ', selection=[('1', 'Till 1'), ('2', 'Till 2'),('3', 'Till 3'), ('4', 'Till 4'),('5', 'Till 5'), ('6', 'Till 6')])
    branch_id_spot_check = fields.Many2one('spot_check.branch',string ='Parent Branch')


