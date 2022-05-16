from odoo import models, fields, api
 
class MobileMoneyNotify(models.Model):
    _inherit = 'spot_check.mobile_money'

    @api.model
    def create(self, values):
        res = super(MobileMoneyNotify, self).create(values)
        spot = self.env['spot_check.vault_setting'].search([('branch_id','=', res.branch_id.id)])
        
        for obj in spot:
            if res.created_on >= obj.from_date and res.created_on <= obj.to_date:
                if obj.currency_type =='UGX' and obj.spot_type=='MM':
                    obj.actual_no
                    obj.spot_check_date = res.created_on
                    obj.actual_no = obj.actual_no + 1

        template_id = self.env.ref('spot_check.email_template_create_teller_request_mm').id
        template =  self.env['mail.template'].browse(template_id)
        template.send_mail(res.id,force_send=True)
        return res
