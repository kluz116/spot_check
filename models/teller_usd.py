from odoo import models,api,fields

class TellersUsd(models.Model):
    _name = "spot_check.teller_usd"
    _inherit="mail.thread"
    _description = "This is a a tellers model"
    _rec_name ="grand_total_ugx"
    
    partner_id = fields.Many2one ('res.partner', 'Accountant', default = lambda self: self.env.user.partner_id )
    from_branch_id = fields.Integer(related='partner_id.branch_id_spot_check.id')
    currency_id = fields.Many2one('res.currency', string='Currency' )
    branch_id = fields.Many2one('spot_check.branch',string ='Branch',domain="[('id','=',from_branch_id)]" ,required=True)
    teller_id = fields.Many2one('res.partner','Teller',domain="[('branch_id_spot_check', '=', branch_id),('user_role','=','teller')]")
    till = fields.Char(string='Till ID',compute='_get_till_id')
    state = fields.Selection([('ongoing', 'Pending Teller Consent'),('confirmed_one', 'Confirmed'),('reject_one', 'Rejected By Teller')],default="ongoing", string="Status")
    hundred_dollar = fields.Monetary(string="$100")
    fifty_dollar = fields.Monetary(string="$50")
    twenty_dollar = fields.Monetary(string="$20")
    ten_dollar = fields.Monetary(string="$10")
    five_dollar = fields.Monetary(string="$5")
    one_dollar = fields.Monetary(string="$1")
    sub_total_good = fields.Monetary(compute='_compute_total_good_currency',string="Sub Total Good Currency",store=True,track_visibility='always')
    mutilated_hundred_dollar = fields.Monetary(string="$100")
    mutilated_fifty_dollar = fields.Monetary(string="$50")
    mutilated_twenty_dollar = fields.Monetary(string="$20")
    mutilated_ten_dollar = fields.Monetary(string="$10")
    mutilated_five_dollar = fields.Monetary(string="$5")
    mutilated_one_dollar = fields.Monetary(string="$1")
    sub_total_mutilated = fields.Monetary(compute='_compute_total_mutilated_currency',string="Sub Total Mutilated",store=True,track_visibility='always')
    grand_total_ugx = fields.Monetary(compute='_compute_grand_totol',string="Grand Total (USD)",store=True)
    system_cash_balance = fields.Monetary(string="System Cash Balance")
    shortage_cash = fields.Monetary(string="Shortage Cash",compute='_get_shortage')
    surplus_cash = fields.Monetary(string="Surplus Cash",compute='_get_surplus')
    created_on =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    trx_proof = fields.Binary(string='Upload Teller Declaration', attachment=True,required=True)
    branch_code = fields.Integer(compute='_compute_branch',string='Branch',store=True)
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
        date_time = self.created_on.strftime("%m%d%Y")
        last= '000'
        self.unique_field = (value or '')+''+(str(self.branch_code))+'-'+(date_time or '')+'-'+(last or '')+''+(str(self.id))
