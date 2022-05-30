from email.policy import default
from odoo import models,api,fields,exceptions

class MobileMoney(models.Model):
    _name = "spot_check.mobile_money"
    _inherit="mail.thread"
    _description = "This is a a tellers model"
    _rec_name ="grand_total_ugx"
    
    partner_id = fields.Many2one ('res.partner', 'Accountant', default = lambda self: self.env.user.partner_id )
    from_branch_id = fields.Integer(related='partner_id.branch_id_spot_check.id')
    currency_id = fields.Many2one('res.currency', string='Currency',default=43 )
    branch_id = fields.Many2one('spot_check.branch',string ='Branch' ,required=True, default = lambda self:self.from_branch_id)
    teller_id = fields.Many2one('res.partner','Teller',domain="[('branch_id_spot_check', '=', branch_id),('user_role','=','teller')]")
    till = fields.Char(string='Till ID',compute='_get_till_id')
    state = fields.Selection([('ongoing', 'Pending Teller Consent'),('confirmed_one', 'Confirmed'),('reject_one', 'Rejected By Teller')],default="ongoing", string="Status")

    grand_total_ugx = fields.Monetary(string="Mobile Balance (UGX)",store=True)
    system_cash_balance = fields.Monetary(string="GL Balance (UGX)",required=True)
    shortage_cash = fields.Monetary(string="Shortage Cash",compute='_get_shortage',store=True)
    surplus_cash = fields.Monetary(string="Surplus Cash",compute='_get_surplus',store=True)
    created_on =  fields.Date(string='Date', default=lambda self: fields.Date.today())
    created_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    trx_proof = fields.Binary(string='GL screen shot', attachment=True,required=True)
    trx_proof1 = fields.Binary(string='Mobile Money Register', attachment=True,required=True)
    trx_proof2 = fields.Binary(string='Mobile Money System Screen Shot', attachment=True,required=True)
    branch_code =  fields.Integer(related='branch_id.branch_code')
    branch_manager = fields.Many2one(compute='_get_manager_id', comodel_name='res.partner', string='Branch Manger', store=True)
    branch_accountant = fields.Many2one(compute='_get_accountant_id', comodel_name='res.partner', string='Branch Accountant', store=True)
    consent_status = fields.Char(string="Consent Status", compute='_get_consent')
    teller_reject_comment = fields.Text(string="Reject Comment")
    reeject_one_date =  fields.Datetime(string='Reject Date')

    consent_comment = fields.Text(string="Comment", required=True, default="Consent Status Yes, Write your comment Here")
    unique_field = fields.Char(string="Ref",compute='comp_name', store=True)
    teller_comment = fields.Text(string="Comment")
    consent_date =  fields.Datetime(string='Consent Date')
   
    
    current_to_branch_accountant = fields.Boolean('is current user ?', compute='_get_to_branch_accountant')
    current_to_branch_manager = fields.Boolean('is current user ?', compute='_get_to_branch_manager')
    current_to_teller = fields.Boolean('is current user ?', compute='_get_to_teller')
    consent_status = fields.Char(string="Consent Status", compute='_get_consent')
    base_url = fields.Char('Base Url', compute='_get_url_id', store='True')
   
    @api.depends('created_on')
    def _get_url_id(self):
        for e in self:
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('spot_check.mobile_money_list_action', raise_if_not_found=False)
            e.base_url = """{}/web#id={}&view_type=form&model=spot_check.mobile_money&action={}""".format(web_base_url,e.id,action_id.id)
    
    
    @api.depends('grand_total_ugx','system_cash_balance')
    def _get_surplus(self):
        for recs in self:
            if recs.grand_total_ugx > recs.system_cash_balance:
                recs.surplus_cash = recs.grand_total_ugx - recs.system_cash_balance
    
    @api.depends('grand_total_ugx','system_cash_balance')
    def _get_shortage(self):
        for rec in self:
            if rec.system_cash_balance == rec.grand_total_ugx:
                rec.shortage_cash = 0
            elif rec.grand_total_ugx < rec.system_cash_balance:
                rec.shortage_cash = rec.grand_total_ugx - rec.system_cash_balance
          
            else:
                rec.shortage_cash = 0

    @api.depends('shortage_cash','surplus_cash')
    def _get_consent(self):
        for record in self:
            if record.shortage_cash < 0:
                record.consent_status = 'Yes'
            elif record.surplus_cash > 0:
                record.consent_status = 'Yes'
            else:
                record.consent_status = 'No'

    

    @api.depends('partner_id')    
    def _get_manager_id(self):
        if self.partner_id:
            self.branch_manager = self.partner_id.supervises

    @api.depends('teller_id')    
    def _get_till_id(self):
        if self.teller_id:
            self.till = self.teller_id.till_id

    @api.depends('branch_manager')    
    def _get_accountant_id(self):
        if self.branch_manager:
            self.branch_accountant = self.branch_manager.supervises  


    @api.depends('branch_accountant')
    def _get_to_branch_accountant(self):
        for e in self:
            partner = self.env['res.users'].browse(self.env.uid).partner_id
            e.current_to_branch_accountant = (True if partner.id == self.branch_accountant.id else False)
 

    @api.depends('branch_manager')
    def _get_to_branch_manager(self):
        for e in self:
            partner = self.env['res.users'].browse(self.env.uid).partner_id
            e.current_to_branch_manager = (True if partner.id == self.branch_manager.id else False)

    @api.depends('teller_id')
    def _get_to_teller(self):
        for e in self:
            partner = self.env['res.users'].browse(self.env.uid).partner_id
            e.current_to_teller = (True if partner.id == self.teller_id.id else False)

    @api.depends('created_on')
    def comp_name(self):
        value = 'SPOT-'
        date_time = self.created_on
        last= '000'
        self.unique_field = (value or '')+''+(str(self.branch_code))+'-'+(date_time or '')+'-'+(last or '')+''+(str(self.id))
    
    @api.one
    @api.constrains('system_cash_balance')
    def _check_system_cash_balance(self):
        if self.system_cash_balance <= 0.0:
            raise exceptions.ValidationError("Sorry, BR System Cash Balance Can Not Be {system_cash_balance} UGX. Please Fill In The Right Figures Before You Proceed. Contact Operations Department for assistance".format(system_cash_balance=self.system_cash_balance))

    
    @api.one
    @api.constrains('branch_id')
    def _checkbranchspotcheck(self):
        pending_conf = self.env['spot_check.mobile_money'].search([('state', 'in', ['ongoing'])])
        for res in pending_conf:
            if  res.branch_id.id == self.branch_id.id and res.state =='ongoing' and res.id is not self.id:
                raise exceptions.ValidationError(f"Hello {res.partner_id.name},  {res.branch_id.branch_name} still has a pending spot check confirmantion  of {res.grand_total_ugx:,.2f} UGX created on {res.created_on} by {res.created_by.name} . Kindly inform Teller {res.teller_id.name} to cosent all the spot checks before you proceed. For any more assistance please contact operations ")

    @api.one
    @api.constrains('created_on')
    def _checkbranchspotcheckToDay(self):
        pending_conf = self.env['spot_check.mobile_money'].search([('state', 'in', ['ongoing','confirmed_one','reject_one'])])
        for res in pending_conf:
            if  res.created_on == self.created_on and res.branch_id.id == self.branch_id.id and res.id is not self.id:
                raise exceptions.ValidationError(f"Hello {res.partner_id.name},  {res.branch_id.branch_name} has already spot checked teller {res.teller_id.name} today of {res.created_on} by {res.created_by.name}. For any more assistance please contact operations cash section.")
      
    

    @api.model
    def _update_notified_pending_confirmation_tellers_mobile_money(self):
        pending_conf = self.env['spot_check.mobile_money'].search([('state', 'not in', ['reject_one','confirmed_one'])])
        for req in pending_conf:
            if req.state =='ongoing':
                template_id = self.env.ref('spot_check.email_template_create_teller_request_mm').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(req.id,force_send=True)