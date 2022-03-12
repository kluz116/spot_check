from odoo import models, fields, api
 
class AtmNotify(models.Model):
    _inherit = 'spot_check.atm'

    @api.model
    def create(self, values):
        res = super(AtmNotify, self).create(values)

        template_id = self.env.ref('spot_check.email_template_create_atm_request').id
        template =  self.env['mail.template'].browse(template_id)
        template.send_mail(res.id,force_send=True)
        return res
