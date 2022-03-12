from odoo import api, fields, models


class SpotCheckRejectAccountant(models.TransientModel):
    _name = "spot_check.reject_accountant"
    _description = "Reject"
    _rec_name = 'state'

    
    state = fields.Selection([('ongoing', 'Pending Accountant Consent'),('confirmed_one', 'Pending Manager Consent'),('rejected_one', 'Rejected By Accountant'),('confirmed_two', 'Confirmed') ,('rejected_two', 'Rejected By Manager')],default="confirmed_one", string="Status")
    accountant_reject_comment = fields.Text(string="Reject Comment")
    reeject_one_date =  fields.Datetime(string='Reject Date', default=lambda self: fields.datetime.now())
    

    @api.multi
    def reject_vault(self):
        self.write({'state': 'rejected_one'})
        spot = self.env['spot_check.vault'].browse(self._context.get('active_ids'))
        for req in spot:
            req.state = self.state
            req.accountant_reject_comment = self.accountant_reject_comment
            req.reeject_one_date = self.reeject_one_date
        
            template_id = self.env.ref('spot_check.email_template_create_vault_request_accountant_rejected').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         
