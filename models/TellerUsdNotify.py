from odoo import models, fields, api
 
class TellerNotifyUsd(models.Model):
    _inherit = 'spot_check.teller_usd'

    @api.model
    def create(self, values):
        res = super(TellerNotifyUsd, self).create(values)

        spot = self.env['spot_check.vault_setting'].search([('branch_id','=', res.branch_id.id)])
        
        for obj in spot:
            if res.created_on >= obj.from_date and res.created_on <= obj.to_date:
                if obj.currency_type =='USD' and obj.spot_type=='Teller':
                    obj.actual_no
                    obj.spot_check_date = res.created_on
                    obj.actual_no = obj.actual_no + 1

        template_id = self.env.ref('spot_check.email_template_create_teller_request_usd').id
        template =  self.env['mail.template'].browse(template_id)
        template.send_mail(res.id,force_send=True)
        return res
