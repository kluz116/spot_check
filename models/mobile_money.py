from email.policy import default
from odoo import models,api,fields,exceptions

class MobileMoney(models.Model):
    _name = "spot_check.mobile_money"
    _inherit="mail.thread"
    _description = "This is a mobile money model"
    _rec_name ="grand_total_ugx"
    
    partner_id = fields.Many2one ('res.partner', 'Name', default = lambda self: self.env.user.partner_id )
    from_branch_id = fields.Integer(related='partner_id.branch_id_spot_check.id')
    currency_id = fields.Many2one('res.currency', string='Currency', default=43)
    branch_id = fields.Many2one('spot_check.branch',string ='Branch', required=True, default=from_branch_id)
    #from_branch_id = fields.Integer(related='branch_id.id')
    branch_accountant = fields.Many2one('res.partner','Accountant',domain="[('branch_id_spot_check', '=', branch_id),('user_role','=','accountant')]")
    branch_manager = fields.Many2one('res.partner','Manager',domain="[('branch_id_spot_check', '=', branch_id),('user_role','=','manager')]")

    state = fields.Selection([('ongoing', 'Pending Accountant Consent'),('confirmed_one', 'Pending Manager Consent'),('rejected_one', 'Rejected By Accountant'),('confirmed_two', 'Confirmed') ,('rejected_two', 'Rejected By Manager')],default="ongoing", string="Status",track_visibility='onchange')
    grand_total_ugx = fields.Monetary(string="Mobile Money Balance",required=True)
    created_on =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    trx_proof = fields.Binary(string='GL screen shot', attachment=True,required=True)
    trx_proof1 = fields.Binary(string='Mobile Money Register', attachment=True,required=True)
    trx_proof2 = fields.Binary(string='Mobile Money System Screen Shot', attachment=True,required=True)
    branch_code = fields.Integer(compute='_compute_branch',string='Branch',store=True)
    #branch_manager = fields.Many2one(compute='_get_manager_id', comodel_name='res.partner', string='Branch Manger', store=True)
    #branch_accountant = fields.Many2one(compute='_get_accountant_id', comodel_name='res.partner', string='Branch Accountant', store=True)
    system_cash_balance = fields.Monetary(string="GL Balance",required=True)
    shortage_cash = fields.Monetary(string="Shortage Cash",compute='_get_shortage')
    surplus_cash = fields.Monetary(string="Surplus Cash",compute='_get_surplus')
    #consent_status = fields.Selection(string='Do you consent that that Vault and System Balance Match?', selection=[('Yes', 'Yes'), ('No', 'No')],track_visibility='always',required=True)
    consent_comment = fields.Text(string="Comment", required=True, default="Consent Status Yes, Write your comment Here")
    unique_field = fields.Char(string="Ref",compute='comp_name', store=True)
    accountant_comment = fields.Text(string="Comment")
    consent_date =  fields.Datetime(string='Consent Date')
    manager_comment = fields.Text(string="Comment")
    consent_manager_date =  fields.Datetime(string='Consent Date')
    accountant_reject_comment = fields.Text(string="Reject Comment")
    reeject_one_date =  fields.Datetime(string='Reject Date')
    manager_reject_comment = fields.Text(string="Reject Comment")
    reeject_two_date =  fields.Datetime(string='Reject Date')
    

    

    

    current_to_branch_accountant = fields.Boolean('is current user ?', compute='_get_to_branch_accountant')
    current_to_branch_manager = fields.Boolean('is current user ?', compute='_get_to_branch_manager')
    consent_status = fields.Char(string="Consent Status", compute='_get_consent')
    base_url = fields.Char('Base Url', compute='_get_url_id', store='True')
   
    @api.depends('created_on')
    def _get_url_id(self):
        for e in self:
            web_base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
            action_id = self.env.ref('spot_check.vault_list_action', raise_if_not_found=False)
            e.base_url = """{}/web#id={}&view_type=form&model=spot_check.vault&action={}""".format(web_base_url,e.id,action_id.id)

    



    
    
        
    
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
            
    @api.depends('user_id')
    def _compute_branch(self):
        for record in self:
            record.branch_code = record.user_id.branch_id_spot_check.branch_code

    @api.depends('partner_id')    
    def _get_manager_id(self):
        if self.partner_id:
            self.branch_manager = self.partner_id.supervises

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

    @api.depends('created_on')
    def comp_name(self):
        value = 'SPOT-'
        date_time = self.created_on.strftime("%m%d%Y")
        last= '000'
        self.unique_field = (value or '')+''+(str(self.branch_code))+'-'+(date_time or '')+'-'+(last or '')+''+(str(self.id))

    @api.one
    @api.constrains('system_cash_balance')
    def _check_system_cash_balance(self):
        if self.system_cash_balance <= 0.0:
            raise exceptions.ValidationError("Sorry, BR System Cash Balance Can Not Be {system_cash_balance} UGX. Please Fill In The Right Figures Before You Proceed. Contact Operations Department for assistance".format(system_cash_balance=self.system_cash_balance))
        
    
        
    