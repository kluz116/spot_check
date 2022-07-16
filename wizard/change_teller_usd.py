from odoo import api, fields, models


class ChangeTellerUsd(models.TransientModel):
    _name = "spot_check.change_teller_usd"
    _description = "Change Tellers"
    _rec_name = 'teller_id'

    
    branch_id = fields.Many2one('spot_check.branch',string ='Branch' ,required=True)
    teller_id = fields.Many2one('res.partner','Teller',domain="[('branch_id_spot_check', '=', branch_id),('user_role','=','teller')]",required=True)

    @api.multi
    def change_teller_usd(self):
        spot = self.env['spot_check.teller_usd'].browse(self._context.get('active_ids'))
        for req in spot:
            req.teller_id = self.teller_id.id
        
        
       
         
