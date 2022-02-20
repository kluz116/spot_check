from odoo import models,api,fields

class Vault(models.Model):
    _name = "spot_check.vault"
    _inherit="mail.thread"
    _description = "This is a a vault model"
    _rec_name ="grand_total_ugx"
    
    partner_id = fields.Many2one ('res.partner', 'Credit supervisor', default = lambda self: self.env.user.partner_id )
    currency_id = fields.Many2one('res.currency', string='Currency' )

    state = fields.Selection([('ongoing', 'Pending Accountant Consent'),('confirmed_one', 'Pending Manager Consent'),('confirmed_two', 'Confirmed')],default="ongoing", string="Status",track_visibility='onchange')
    deno_fifty_thounsand = fields.Monetary(string="50,000 Shs")
    deno_twenty_thounsand = fields.Monetary(string="20,000 Shs")
    deno_ten_thounsand = fields.Monetary(string="10,000 Shs")
    deno_five_thounsand = fields.Monetary(string="5,000 Shs")
    deno_two_thounsand = fields.Monetary(string="2,000 Shs")
    deno_one_thounsand = fields.Monetary(string="1,000 Shs")
    sub_total_good = fields.Float(compute='_compute_total_good_currency',string="Sub Total Good Currency",store=True,track_visibility='always')
    coin_one_thounsand = fields.Monetary(string="1,000 Shs")
    coin_five_houndred = fields.Monetary(string="500 Shs")
    coin_two_hundred = fields.Monetary(string="200 Shs")
    coin_one_hundred = fields.Monetary(string="100 Shs")
    coin_fifty = fields.Monetary(string="50 Shs")
    sub_total_coins = fields.Monetary(compute='_compute_total_coins',string="Sub Total Coins",store=True,track_visibility='always')
    mutilated_deno_fifty_thounsand = fields.Monetary(string="50,000 Shs")
    mutilated_deno_twenty_thounsand = fields.Monetary(string="20,000 Shs")
    mutilated_deno_ten_thounsand = fields.Monetary(string="10,000 Shs")
    mutilated_deno_five_thounsand = fields.Monetary(string="5,000 Shs")
    mutilated_deno_two_thounsand = fields.Monetary(string="2,000 Shs")
    mutilated_deno_one_thounsand = fields.Monetary(string="1,000 Shs")
    sub_total_mutilated = fields.Monetary(compute='_compute_total_mutilated_currency',string="Sub Total Mutilated",store=True,track_visibility='always')
    grand_total_ugx = fields.Monetary(compute='_compute_grand_totol',string="Grand Total (UGX)",store=True)
    created_on =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    trx_proof = fields.Binary(string='Upload file', attachment=True,required=True)
    branch_code = fields.Integer(compute='_compute_branch',string='Branch',store=True)
    branch_manager = fields.Many2one(compute='_get_manager_id', comodel_name='res.partner', string='Branch Manger', store=True)
    branch_accountant = fields.Many2one(compute='_get_accountant_id', comodel_name='res.partner', string='Branch Accountant', store=True)
    system_cash_balance = fields.Monetary(string="System Cash Balance")
    shortage_cash = fields.Monetary(string="Shortage Cash")
    surplus_cash = fields.Monetary(string="Surplus Cash")
    consent_status = fields.Selection(string='Do you consent that that Vault and System Balance Match?', selection=[('Yes', 'Yes'), ('No', 'No')],track_visibility='always')
    consent_comment = fields.Text(string="Comment")
    unique_field = fields.Char(string="Ref",compute='comp_name', store=True)
    accountant_comment = fields.Text(string="Comment")
    consent_date =  fields.Datetime(string='Consent Date')
    manager_comment = fields.Text(string="Comment")
    consent_manager_date =  fields.Datetime(string='Consent Date')
    

    current_to_branch_accountant = fields.Boolean('is current user ?', compute='_get_to_branch_accountant')
    current_to_branch_manager = fields.Boolean('is current user ?', compute='_get_to_branch_manager')
    


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

    
    @api.depends('user_id')
    def _compute_branch(self):
        for record in self:
            record.branch_code = record.user_id.branch_id.branch_code

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

  
    
        
    