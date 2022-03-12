from odoo import models, fields, api
 
class TellerNotify(models.Model):
    _inherit = 'spot_check.teller'

    @api.model
    def create(self, values):
        res = super(TellerNotify, self).create(values)

        template_id = self.env.ref('spot_check.email_template_create_teller_request_consent').id
        template =  self.env['mail.template'].browse(template_id)
        template.send_mail(res.id,force_send=True)
        return res
