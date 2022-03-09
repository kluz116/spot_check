from odoo import api, fields, models


class SpotCheckRejectTeller(models.TransientModel):
    _name = "spot_check.cash_reject_teller"
    _description = "Reject"
    _rec_name = 'state'

    
    state = fields.Selection([('ongoing', 'Teller Consent'),('confirmed_one', 'Confirmed'),('reject_one', 'Rejected By Teller')],default="reject_one", string="Status")
    teller_reject_comment = fields.Text(string="Reject Comment")
    reeject_one_date =  fields.Datetime(string='Reject Date', default=lambda self: fields.datetime.now())
    

    @api.multi
    def reject_teller(self):
        self.write({'state': 'reject_one'})
        spot = self.env['spot_check.teller'].browse(self._context.get('active_ids'))
        for req in spot:
            req.state = self.state
            req.teller_reject_comment = self.teller_reject_comment
            req.reeject_one_date = self.reeject_one_date
        
            #template_id = self.env.ref('cash_managment.email_template_branch_bank_request_confirm').id
            #template =  self.env['mail.template'].browse(template_id)
            #template.send_mail(req.id,force_send=True)
         
