from odoo import api, fields, models


class SpotCheckRejectAccountantATM(models.TransientModel):
    _name = "spot_check.atm_reject_accountant"
    _description = "Reject"
    _rec_name = 'state'

    
    state = fields.Selection([('ongoing', 'Pending Accountant Consent'),('confirmed_one', 'Pending Manager Consent'),('rejected_one', 'Rejected By Accountant'),('confirmed_two', 'Confirmed') ,('rejected_two', 'Rejected By Manager')],default="confirmed_one", string="Status")
    accountant_reject_comment = fields.Text(string="Reject Comment")
    reeject_one_date =  fields.Datetime(string='Reject Date', default=lambda self: fields.datetime.now())
    

    @api.multi
    def reject_atm(self):
        self.write({'state': 'rejected_one'})
        spot = self.env['spot_check.atm'].browse(self._context.get('active_ids'))
        for req in spot:
            req.state = self.state
            req.accountant_reject_comment = self.accountant_reject_comment
            req.reeject_one_date = self.reeject_one_date
        
            #template_id = self.env.ref('cash_managment.email_template_branch_bank_request_confirm').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         
