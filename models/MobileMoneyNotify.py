from odoo import models, fields, api
 
class MobileMoneyNotify(models.Model):
    _inherit = 'spot_check.mobile_money'

    @api.model
    def create(self, values):
        res = super(MobileMoneyNotify, self).create(values)

        template_id = self.env.ref('spot_check.email_template_create_mm_request').id
        template =  self.env['mail.template'].browse(template_id)
        template.send_mail(res.id,force_send=True)
        return res
