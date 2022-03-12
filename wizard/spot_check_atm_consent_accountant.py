from odoo import api, fields, models


class SpotCheckConsentAccountantATM(models.TransientModel):
    _name = "spot_check.consent_accountant_atm"
    _description = "Confirm"
    _rec_name = 'state'

    
    state = fields.Selection([('ongoing', 'Pending Accountant Consent'),('confirmed_one', 'Pending Manager Consent'),('confirmed_two', 'Confirmed')],default="confirmed_one", string="Status")
    accountant_comment = fields.Text(string="Comment")
    consent_date =  fields.Datetime(string='Consent Date', default=lambda self: fields.datetime.now())
    

    @api.multi
    def consent_atm(self):
        self.write({'state': 'confirmed_one'})
        spot = self.env['spot_check.atm'].browse(self._context.get('active_ids'))
        for req in spot:
            req.state = self.state
            req.accountant_comment = self.accountant_comment
            req.consent_date = self.consent_date
        
            template_id = self.env.ref('spot_check.email_template_create_atm_request_to_manager').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         
