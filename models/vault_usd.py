from odoo import models,api,fields,exceptions

class VaultUsd(models.Model):
    _name = "spot_check.vault_usd"
    _inherit="mail.thread"
    _description = "This is a a vault model"
    _rec_name ="grand_total_ugx"
    
    partner_id = fields.Many2one ('res.partner', 'Credit supervisor', default = lambda self: self.env.user.partner_id )
    currency_id = fields.Many2one('res.currency', string='Currency',default=2  )

    state = fields.Selection([('ongoing', 'Pending Accountant Consent'),('confirmed_one', 'Pending Manager Consent'),('rejected_one', 'Rejected By Accountant'),('confirmed_two', 'Confirmed') ,('rejected_two', 'Rejected By Manager')],default="ongoing", string="Status",track_visibility='onchange')
    hundred_dollar_count = fields.Integer(string="100 Notes")
    hundred_dollar = fields.Monetary(string="$100", compute='_compute_hundred_dollar')
    fifty_dollar_count = fields.Integer(string="50 Notes")
    fifty_dollar = fields.Monetary(string="$50",compute='_compute_fifty_dollar')
    twenty_dollar_count = fields.Integer(string="20 Notes")
    twenty_dollar = fields.Monetary(string="$20",compute='_compute_twenty_dollar')
    ten_dollar_count = fields.Integer(string="10 Notes")
    ten_dollar = fields.Monetary(string="$10",compute='_compute_ten_dollar')
    five_dollar_count = fields.Integer(string="5 Notes")
    five_dollar = fields.Monetary(string="$5",compute='_compute_five_dollar')
    one_dollar_count = fields.Integer(string="1 Notes")
    one_dollar = fields.Monetary(string="$1",compute='_compute_one_dollar')
    sub_total_good = fields.Monetary(compute='_compute_total_good_currency',string="Sub Total Good Currency",store=True,track_visibility='always')
    mutilated_hundred_dollar_count = fields.Integer(string="100 Notes")
    mutilated_hundred_dollar = fields.Monetary(string="$100", compute='_compute_mutilated_hundred_dollar')
    mutilated_fifty_dollar_count = fields.Integer(string="50 Notes")
    mutilated_fifty_dollar = fields.Monetary(string="$50",compute='_compute_mutilated_fifty_dollar')
    mutilated_twenty_dollar_count = fields.Integer(string="20 Notes")
    mutilated_twenty_dollar = fields.Monetary(string="$20",compute='_compute_mutilated_twenty_dollar')
    mutilated_ten_dollar_count = fields.Integer(string="10 Notes")
    mutilated_ten_dollar = fields.Monetary(string="$10",compute='_compute_mutilated_ten_dollar')
    mutilated_five_dollar_count = fields.Integer(string="5 Notes")
    mutilated_five_dollar = fields.Monetary(string="$5",compute='_compute_mutilated_five_dollar')
    mutilated_one_dollar_count = fields.Integer(string="1 Notes")
    mutilated_one_dollar = fields.Monetary(string="$1",compute='_compute_mutilated_one_dollar')

    sub_total_mutilated = fields.Monetary(compute='_compute_total_mutilated_currency',string="Sub Total Mutilated",store=True,track_visibility='always')
    grand_total_ugx = fields.Monetary(compute='_compute_grand_totol',string="Grand Total (USD)",store=True)
    created_on =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    trx_proof = fields.Binary(string='Upload BRNET GL', attachment=True,required=True)
    branch_code = fields.Integer(compute='_compute_branch',string='Branch',store=True)
    branch_manager = fields.Many2one(compute='_get_manager_id', comodel_name='res.partner', string='Branch Manger', store=True)
    branch_accountant = fields.Many2one(compute='_get_accountant_id', comodel_name='res.partner', string='Branch Accountant', store=True)
    system_cash_balance = fields.Monetary(string="System Cash Balance")
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
            action_id = self.env.ref('spot_check.teller_list_action_usd', raise_if_not_found=False)
            e.base_url = """{}/web#id={}&view_type=form&model=spot_check.vault&action={}""".format(web_base_url,e.id,action_id.id)

    
    @api.depends('mutilated_hundred_dollar_count')
    def _compute_mutilated_hundred_dollar(self):
        for record in self:
           record.mutilated_hundred_dollar = record.mutilated_hundred_dollar_count * 100

    @api.depends('mutilated_fifty_dollar_count')
    def _compute_mutilated_fifty_dollar(self):
        for record in self:
           record.mutilated_fifty_dollar = record.mutilated_fifty_dollar_count * 50

    @api.depends('mutilated_twenty_dollar_count')
    def _compute_mutilated_twenty_dollar(self):
        for record in self:
           record.mutilated_twenty_dollar = record.mutilated_twenty_dollar_count * 20

    @api.depends('mutilated_ten_dollar_count')
    def _compute_mutilated_ten_dollar(self):
        for record in self:
           record.mutilated_ten_dollar = record.mutilated_ten_dollar_count * 10

    @api.depends('mutilated_five_dollar_count')
    def _compute_mutilated_five_dollar(self):
        for record in self:
           record.mutilated_five_dollar = record.mutilated_five_dollar_count * 5

    @api.depends('mutilated_one_dollar_count')
    def _compute_mutilated_one_dollar(self):
        for record in self:
           record.mutilated_one_dollar = record.mutilated_one_dollar_count * 1


    


    
    @api.depends('hundred_dollar_count')
    def _compute_hundred_dollar(self):
        for record in self:
           record.hundred_dollar = record.hundred_dollar_count * 100

    @api.depends('fifty_dollar_count')
    def _compute_fifty_dollar(self):
        for record in self:
           record.fifty_dollar = record.fifty_dollar_count * 50

    @api.depends('twenty_dollar_count')
    def _compute_twenty_dollar(self):
        for record in self:
           record.twenty_dollar = record.twenty_dollar_count * 20

    @api.depends('ten_dollar_count')
    def _compute_ten_dollar(self):
        for record in self:
           record.ten_dollar = record.ten_dollar_count * 10

    @api.depends('five_dollar_count')
    def _compute_five_dollar(self):
        for record in self:
           record.five_dollar = record.five_dollar_count * 5

    @api.depends('one_dollar_count')
    def _compute_one_dollar(self):
        for record in self:
           record.one_dollar = record.one_dollar_count * 1



    @api.depends('hundred_dollar', 'fifty_dollar','twenty_dollar','ten_dollar','five_dollar','one_dollar')
    def _compute_total_good_currency(self):
        for record in self:
            record.sub_total_good = record.hundred_dollar + record.fifty_dollar + record.twenty_dollar + record.five_dollar + record.one_dollar + record.ten_dollar
        
    @api.depends('mutilated_hundred_dollar', 'mutilated_fifty_dollar','mutilated_twenty_dollar','mutilated_ten_dollar','mutilated_five_dollar','mutilated_one_dollar')
    def _compute_total_mutilated_currency(self):
        for record in self:
            record.sub_total_mutilated = record.mutilated_hundred_dollar + record.mutilated_fifty_dollar + record.mutilated_twenty_dollar + record.mutilated_ten_dollar + record.mutilated_five_dollar + record.mutilated_one_dollar

    @api.depends('sub_total_good','sub_total_mutilated')
    def _compute_grand_totol(self):
        for record in self:
           record.grand_total_ugx = record.sub_total_good + record.sub_total_mutilated 

    
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
            raise exceptions.ValidationError("Sorry, BR System Cash Balance Can Not Be {system_cash_balance} USD. Please Fill In The Right Figures Before You Proceed. Contact Operations Department for assistance".format(system_cash_balance=self.system_cash_balance))
        
        
    