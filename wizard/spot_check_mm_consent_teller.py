from odoo import api, fields, models


class SpotCheckConsentTellerMM(models.TransientModel):
    _name = "spot_check.consent_teller_mm"
    _description = "Confirm"
    _rec_name = 'state'

    
    state = fields.Selection([('ongoing', 'Teller Consent'),('confirmed_one', 'Confirmed')],default="confirmed_one", string="Status")
    teller_comment = fields.Text(string="Comment")
    consent_date =  fields.Datetime(string='Consent Date', default=lambda self: fields.datetime.now())
    

    @api.multi
    def consent_teller_mm(self):
        self.write({'state': 'confirmed_one'})
        spot = self.env['spot_check.mobile_money'].browse(self._context.get('active_ids'))
        for req in spot:
            req.state = self.state
            req.teller_comment = self.teller_comment
            req.consent_date = self.consent_date
        
            template_id = self.env.ref('spot_check.email_template_create_teller_request_consent_mm').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         
