from odoo import models, fields, api
 
class VaultNotifyUsd(models.Model):
    _inherit = 'spot_check.vault_usd'

    @api.model
    def create(self, values):
        res = super(VaultNotifyUsd, self).create(values)

        template_id = self.env.ref('spot_check.email_template_create_vault_request_usd').id
        template =  self.env['mail.template'].browse(template_id)
        template.send_mail(res.id,force_send=True)
        return res
