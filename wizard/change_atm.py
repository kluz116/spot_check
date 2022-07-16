from odoo import api, fields, models


class ChangeAtm(models.TransientModel):
    _name = "spot_check.change_atm"
    _description = "Change Atm"
    _rec_name = 'branch_accountant'

    
    branch_id = fields.Many2one('spot_check.branch',string ='Branch', required=True)
    branch_accountant = fields.Many2one('res.partner','Accountant',domain="[('branch_id_spot_check', '=', branch_id),('user_role','=','accountant')]")
    branch_manager = fields.Many2one('res.partner','Manager',domain="[('branch_id_spot_check', '=', branch_id),('user_role','=','manager')]")


    @api.multi
    def change_atm_(self):
        spot = self.env['spot_check.atm'].browse(self._context.get('active_ids'))
        for req in spot:
            req.branch_accountant = self.branch_accountant.id
            req.branch_manager = self.branch_manager.id
        
        
       
         
