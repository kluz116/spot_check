from odoo import api, fields, models


class SpotCheckConsentManagerMM(models.TransientModel):
    _name = "spot_check.consent_manager_mm"
    _description = "Confirm"
    _rec_name = 'state'

    
    state = fields.Selection([('ongoing', 'Pending Accountant Consent'),('confirmed_one', 'Pending Manager Consent'),('confirmed_two', 'Confirmed')],default="confirmed_one", string="Status")
    manager_comment = fields.Text(string="Comment")
    consent_manager_date =  fields.Datetime(string='Consent Date', default=lambda self: fields.datetime.now())
    

    @api.multi
    def consent_mm_manager(self):
        self.write({'state': 'confirmed_two'})
        spot = self.env['spot_check.mobile_money'].browse(self._context.get('active_ids'))
        for req in spot:
            req.state = self.state
            req.manager_comment = self.manager_comment
            req.consent_manager_date = self.consent_manager_date
        
            template_id = self.env.ref('spot_check.email_template_create_mm_request_final').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         
