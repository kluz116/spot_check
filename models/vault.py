from odoo import models,api,fields,exceptions

class Vault(models.Model):
    _name = "spot_check.vault"
    _inherit="mail.thread"
    _description = "This is a a vault model"
    _rec_name ="grand_total_ugx"
    
    partner_id = fields.Many2one ('res.partner', 'Credit supervisor', default = lambda self: self.env.user.partner_id )
    currency_id = fields.Many2one('res.currency', string='Currency' )

    state = fields.Selection([('ongoing', 'Pending Accountant Consent'),('confirmed_one', 'Pending Manager Consent'),('rejected_one', 'Rejected By Accountant'),('confirmed_two', 'Confirmed') ,('rejected_two', 'Rejected By Manager')],default="ongoing", string="Status",track_visibility='onchange')
    deno_fifty_thounsand_count = fields.Integer(string="50,000 Notes")
    deno_fifty_thounsand = fields.Monetary(compute='_compute_deno_fifty_thounsand',string="50,000 Shs")
    deno_twenty_thounsand_count = fields.Integer(string="20,000 Notes")
    deno_twenty_thounsand = fields.Monetary(compute='_compute_deno_twenty_thounsand',string="20,000 Shs")
    deno_ten_thounsand_count = fields.Integer(string="10,000 Notes")
    deno_ten_thounsand = fields.Monetary(string="10,000 Shs",compute='_compute_deno_ten_thounsand')
    deno_five_thounsand_count = fields.Integer(string="5,000 Notes")
    deno_five_thounsand = fields.Monetary(string="5,000 Shs" ,compute='_compute_deno_five_thounsand')
    deno_two_thounsand_count = fields.Integer(string="2,000 Notes")
    deno_two_thounsand = fields.Monetary(string="2,000 Shs" ,compute='_compute_deno_two_thounsand')
    deno_one_thounsand_count = fields.Integer(string="1,000 Notes")
    deno_one_thounsand = fields.Monetary(string="1,000 Shs",compute='_compute_deno_one_thounsand')
    sub_total_good = fields.Monetary(compute='_compute_total_good_currency',string="Sub Total Good Currency",store=True,track_visibility='always')

    coin_one_thounsand_count = fields.Integer(string="1,000 Coins")
    coin_one_thounsand = fields.Monetary(string="1,000 Shs", compute='_compute_coin_one_thounsand')
    coin_five_houndred_count = fields.Integer(string="500 Coins")
    coin_five_houndred = fields.Monetary(string="500 Shs",compute='_compute_coin_five_houndred')
    coin_two_hundred_count = fields.Integer(string="200 Coins")
    coin_two_hundred = fields.Monetary(string="200 Shs",compute='_compute_coin_two_hundred')
    coin_one_hundred_count = fields.Integer(string="100 Coins")
    coin_one_hundred = fields.Monetary(string="100 Shs",compute='_compute_coin_one_hundred')
    coin_fifty_count = fields.Integer(string="50 Coins")
    coin_fifty = fields.Monetary(string="50 Shs", compute='_compute_coin_fifty')
    
    sub_total_coins = fields.Monetary(compute='_compute_total_coins',string="Sub Total Coins",store=True,track_visibility='always')

    mutilated_deno_fifty_thounsand_count = fields.Integer(string="50,000 Notes")
    mutilated_deno_fifty_thounsand = fields.Monetary(compute='_compute_deno_fifty_thounsand_mutilated_',string="50,000 Shs")
    mutilated_deno_twenty_thounsand_count = fields.Integer(string="20,000 Notes")
    mutilated_deno_twenty_thounsand = fields.Monetary(compute='_compute_deno_twenty_thounsand_mutilated_',string="20,000 Shs")
    mutilated_deno_ten_thounsand_count = fields.Integer(string="10,000 Notes")
    mutilated_deno_ten_thounsand = fields.Monetary(string="10,000 Shs",compute='_compute_deno_ten_thounsand_mutilated_')
    mutilated_deno_five_thounsand_count = fields.Integer(string="5,000 Notes")
    mutilated_deno_five_thounsand = fields.Monetary(string="5,000 Shs" ,compute='_compute_deno_five_thounsand_mutilated_')
    mutilated_deno_two_thounsand_count = fields.Integer(string="2,000 Notes")
    mutilated_deno_two_thounsand = fields.Monetary(string="2,000 Shs" ,compute='_compute_deno_two_thounsand_mutilated_')
    mutilated_deno_one_thounsand_count = fields.Integer(string="1,000 Notes")
    mutilated_deno_one_thounsand = fields.Monetary(string="2,000 Shs" ,compute='_compute_deno_one_thounsand_mutilated_')

    sub_total_mutilated = fields.Monetary(compute='_compute_total_mutilated_currency',string="Sub Total Mutilated",store=True,track_visibility='always')
    grand_total_ugx = fields.Monetary(compute='_compute_grand_totol',string="Grand Total (UGX)",store=True)
    created_on =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    trx_proof = fields.Binary(string='Upload BRNET GL', attachment=True,required=True)
    branch_code = fields.Integer(compute='_compute_branch',string='Branch',store=True)
    branch_manager = fields.Many2one(compute='_get_manager_id', comodel_name='res.partner', string='Branch Manger', store=True)
    branch_accountant = fields.Many2one(compute='_get_accountant_id', comodel_name='res.partner', string='Branch Accountant', store=True)
    system_cash_balance = fields.Monetary(string="System Cash Balance",required=True)
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

    

    @api.depends('deno_fifty_thounsand', 'deno_twenty_thounsand','deno_ten_thounsand','deno_five_thounsand','deno_two_thounsand','deno_one_thounsand')
    def _compute_total_good_currency(self):
        for record in self:
            record.sub_total_good = record.deno_fifty_thounsand + record.deno_twenty_thounsand + record.deno_ten_thounsand + record.deno_five_thounsand + record.deno_two_thounsand + record.deno_one_thounsand
        
    @api.depends('coin_one_thounsand','coin_five_houndred','coin_two_hundred','coin_one_hundred','coin_fifty')
    def _compute_total_coins(self):
        for record in self:
            record.sub_total_coins =  record.coin_one_thounsand + record.coin_five_houndred + record.coin_two_hundred + record.coin_one_hundred + record.coin_fifty

    @api.depends('mutilated_deno_fifty_thounsand', 'mutilated_deno_twenty_thounsand','mutilated_deno_ten_thounsand','mutilated_deno_five_thounsand','mutilated_deno_two_thounsand','mutilated_deno_one_thounsand')
    def _compute_total_mutilated_currency(self):
        for record in self:
            record.sub_total_mutilated = record.mutilated_deno_fifty_thounsand + record.mutilated_deno_twenty_thounsand + record.mutilated_deno_ten_thounsand + record.mutilated_deno_five_thounsand + record.mutilated_deno_two_thounsand + record.mutilated_deno_one_thounsand

    @api.depends('sub_total_good', 'sub_total_coins','sub_total_mutilated')
    def _compute_grand_totol(self):
        for record in self:
           record.grand_total_ugx = record.sub_total_good + record.sub_total_coins + record.sub_total_mutilated 

    @api.depends('mutilated_deno_fifty_thounsand_count')
    def _compute_deno_fifty_thounsand_mutilated_(self):
        for record in self:
           record.mutilated_deno_fifty_thounsand = record.mutilated_deno_fifty_thounsand_count * 50000
    
    @api.depends('mutilated_deno_twenty_thounsand_count')
    def _compute_deno_twenty_thounsand_mutilated_(self):
        for record in self:
           record.mutilated_deno_twenty_thounsand = record.mutilated_deno_twenty_thounsand_count * 20000

    @api.depends('mutilated_deno_ten_thounsand_count')
    def _compute_deno_ten_thounsand_mutilated_(self):
        for record in self:
           record.mutilated_deno_ten_thounsand = record.mutilated_deno_ten_thounsand_count * 10000

    @api.depends('mutilated_deno_five_thounsand_count')
    def _compute_deno_five_thounsand_mutilated_(self):
        for record in self:
           record.mutilated_deno_five_thounsand = record.mutilated_deno_five_thounsand_count * 5000

    @api.depends('mutilated_deno_two_thounsand_count')
    def _compute_deno_two_thounsand_mutilated_(self):
        for record in self:
           record.mutilated_deno_two_thounsand = record.mutilated_deno_two_thounsand_count * 2000

    @api.depends('mutilated_deno_one_thounsand_count')
    def _compute_deno_one_thounsand_mutilated_(self):
        for record in self:
           record.mutilated_deno_one_thounsand = record.mutilated_deno_one_thounsand_count * 1000


    
    @api.depends('coin_one_thounsand_count')
    def _compute_coin_one_thounsand(self):
        for record in self:
            record.coin_one_thounsand = record.coin_one_thounsand_count * 1000
     
    @api.depends('coin_five_houndred_count')
    def _compute_coin_five_houndred(self):
        for record in self:
            record.coin_five_houndred = record.coin_five_houndred_count * 500

    @api.depends('coin_two_hundred_count')
    def _compute_coin_two_hundred(self):
        for record in self:
            record.coin_two_hundred = record.coin_two_hundred_count * 500

    
    @api.depends('coin_one_hundred_count')
    def _compute_coin_two_hundred(self):
        for record in self:
            record.coin_one_hundred = record.coin_one_hundred_count *100

    @api.depends('coin_fifty_count')
    def _compute_coin_fifty(self):
        for record in self:
            record.coin_fifty = record.coin_fifty_count *50

            

    
    
            




    
    @api.depends('deno_fifty_thounsand_count')
    def _compute_deno_fifty_thounsand(self):
        for record in self:
           record.deno_fifty_thounsand = record.deno_fifty_thounsand_count * 50000
    
    @api.depends('deno_twenty_thounsand_count')
    def _compute_deno_twenty_thounsand(self):
        for record in self:
           record.deno_twenty_thounsand = record.deno_twenty_thounsand_count * 20000

    @api.depends('deno_ten_thounsand_count')
    def _compute_deno_ten_thounsand(self):
        for record in self:
           record.deno_ten_thounsand = record.deno_ten_thounsand_count * 10000

    @api.depends('deno_five_thounsand_count')
    def _compute_deno_five_thounsand(self):
        for record in self:
           record.deno_five_thounsand = record.deno_five_thounsand_count * 5000

    @api.depends('deno_two_thounsand_count')
    def _compute_deno_two_thounsand(self):
        for record in self:
           record.deno_two_thounsand = record.deno_two_thounsand_count * 2000

    @api.depends('deno_one_thounsand_count')
    def _compute_deno_one_thounsand(self):
        for record in self:
           record.deno_one_thounsand = record.deno_one_thounsand_count * 1000

    

    
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
    def _check_hours(self):
        if self.system_cash_balance < 0:
            raise exceptions.ValidationError("Sorry, System Cash Balance Can Not Be {system_cash_balance}. Please Fill In The Right Figures Before You Proceed. Contact Operations Department for assistance".format(system_cash_balance=system_cash_balance))
        
    
        
    