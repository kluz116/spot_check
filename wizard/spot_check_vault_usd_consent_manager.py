from odoo import api, fields, models


class SpotCheckConsentManagerUsd(models.TransientModel):
    _name = "spot_check.consent_manager_usd"
    _description = "Confirm"
    _rec_name = 'state'

    
    state = fields.Selection([('ongoing', 'Pending Accountant Consent'),('confirmed_one', 'Pending Manager Consent'),('confirmed_two', 'Confirmed')],default="confirmed_one", string="Status")
    manager_comment = fields.Text(string="Comment")
    consent_manager_date =  fields.Datetime(string='Consent Date', default=lambda self: fields.datetime.now())
    

    @api.multi
    def consent_vault_manager_usd(self):
        self.write({'state': 'confirmed_two'})
        spot = self.env['spot_check.vault_usd'].browse(self._context.get('active_ids'))
        for req in spot:
            req.state = self.state
            req.manager_comment = self.manager_comment
            req.consent_manager_date = self.consent_manager_date
        
            template_id = self.env.ref('spot_check.email_template_create_vault_request_final_usd').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         
