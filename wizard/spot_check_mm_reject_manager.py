from odoo import api, fields, models


class SpotCheckRejectManagerMM(models.TransientModel):
    _name = "spot_check.reject_manager_mm"
    _description = "Reject"
    _rec_name = 'state'

    
    state = fields.Selection([('ongoing', 'Pending Accountant Consent'),('confirmed_one', 'Pending Manager Consent'),('rejected_one', 'Rejected By Accountant'),('confirmed_two', 'Confirmed') ,('rejected_two', 'Rejected By Manager')],default="confirmed_one", string="Status")
    manager_reject_comment = fields.Text(string="Reject Comment")
    reeject_two_date =  fields.Datetime(string='Reject Date', default=lambda self: fields.datetime.now())
    

    @api.multi
    def reject_mm_manager(self):
        self.write({'state': 'rejected_two'})
        spot = self.env['spot_check.mobile_money'].browse(self._context.get('active_ids'))
        for req in spot:
            req.state = self.state
            req.manager_reject_comment = self.manager_reject_comment
            req.reeject_two_date = self.reeject_two_date
        
            template_id = self.env.ref('spot_check.email_template_create_mm_request_manager_rejected').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(req.id,force_send=True)
         
