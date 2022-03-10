from odoo import api, fields, models


class SpotCheckConsentTellerUsd(models.TransientModel):
    _name = "spot_check.consent_teller_usd"
    _description = "Confirm"
    _rec_name = 'state'

    
    state = fields.Selection([('ongoing', 'Teller Consent'),('confirmed_one', 'Confirmed')],default="confirmed_one", string="Status")
    teller_comment = fields.Text(string="Comment")
    consent_date =  fields.Datetime(string='Consent Date', default=lambda self: fields.datetime.now())
    

    @api.multi
    def consent_teller_usd(self):
        self.write({'state': 'confirmed_one'})
        spot = self.env['spot_check.teller_usd'].browse(self._context.get('active_ids'))
        for req in spot:
            req.state = self.state
            req.teller_comment = self.teller_comment
            req.consent_date = self.consent_date
        
            #template_id = self.env.ref('cash_managment.email_template_branch_bank_request_confirm').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         
