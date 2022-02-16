from odoo import api, fields, models


class SpotCheckConsentManagerATM(models.TransientModel):
    _name = "spot_check.consent_manager_atm"
    _description = "Confirm"
    _rec_name = 'state'

    
    state = fields.Selection([('ongoing', 'Pending Accountant Consent'),('confirmed_one', 'Pending Manager Consent'),('confirmed_two', 'Confirmed')],default="confirmed_one", string="Status")
    manager_comment = fields.Text(string="Comment")
    consent_manager_date =  fields.Datetime(string='Consent Date', default=lambda self: fields.datetime.now())
    

    @api.multi
    def consent_atm_manager(self):
        self.write({'state': 'confirmed_two'})
        spot = self.env['spot_check.atm'].browse(self._context.get('active_ids'))
        for req in spot:
            req.state = self.state
            req.manager_comment = self.manager_comment
            req.consent_manager_date = self.consent_manager_date
        
            #template_id = self.env.ref('cash_managment.email_template_branch_bank_request_confirm').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         
