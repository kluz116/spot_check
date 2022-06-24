from odoo import models,api,fields,exceptions
import datetime

class Tellers(models.Model):
    _name = "spot_check.teller"
    _inherit="mail.thread"
    _description = "This is a a tellers model"
    _rec_name ="grand_total_ugx"
    
    partner_id = fields.Many2one ('res.partner', 'Accountant', default = lambda self: self.env.user.partner_id )
    from_branch_id = fields.Integer(related='partner_id.branch_id_spot_check.id')
    currency_id = fields.Many2one('res.currency', string='Currency',default=43 )
    branch_id = fields.Many2one('spot_check.branch',string ='Branch' ,required=True)
    teller_id = fields.Many2one('res.partner','Teller',domain="[('branch_id_spot_check', '=', branch_id),('user_role','=','teller')]",required=True)
    till = fields.Char(string='Till ID',compute='_get_till_id',required=True)
    state = fields.Selection([('ongoing', 'Pending Teller Consent'),('confirmed_one', 'Confirmed'),('reject_one', 'Rejected By Teller')],default="ongoing", string="Status")
    
    deno_fifty_thounsand_bundle = fields.Integer(string="Bundles")
    deno_fifty_thounsand_count = fields.Integer(string="50,000 Loose Notes")
    deno_fifty_thounsand = fields.Monetary(compute='_compute_deno_fifty_thounsand',string="Total 50,000 Shs",store=True)
    deno_twenty_thounsand_bundle = fields.Integer(string="Bundles")
    deno_twenty_thounsand_count = fields.Integer(string="20,000 Loose Notes")
    deno_twenty_thounsand = fields.Monetary(compute='_compute_deno_twenty_thounsand',string="20,000 Shs",store=True)
    deno_ten_thounsand_bundle = fields.Integer(string="Bundles")
    deno_ten_thounsand_count = fields.Integer(string="10,000 Loose Notes")
    deno_ten_thounsand = fields.Monetary(string="10,000 Shs",compute='_compute_deno_ten_thounsand',store=True)
    deno_five_thounsand_bundle = fields.Integer(string="Bundles")
    deno_five_thounsand_count = fields.Integer(string="5,000 Loose Notes")
    deno_five_thounsand = fields.Monetary(string="5,000 Shs" ,compute='_compute_deno_five_thounsand',store=True)
    deno_two_thounsand_bundle = fields.Integer(string="Bundles")
    deno_two_thounsand_count = fields.Integer(string="2,000 Loose Notes")
    deno_two_thounsand = fields.Monetary(string="2,000 Shs" ,compute='_compute_deno_two_thounsand',store=True)
    deno_one_thounsand_bundle = fields.Integer(string="Bundles")
    deno_one_thounsand_count = fields.Integer(string="1,000 Loose Notes")
    deno_one_thounsand = fields.Monetary(string="1,000 Shs",compute='_compute_deno_one_thounsand',store=True)
    sub_total_good = fields.Monetary(compute='_compute_total_good_currency',string="Sub Total Good Currency",store=True,track_visibility='always')
    coin_one_thounsand_bundle = fields.Integer(string="Bundles")
    coin_one_thounsand_count = fields.Integer(string="1,000 Coins")
    coin_one_thounsand = fields.Monetary(string="1,000 Shs", compute='_compute_coin_one_thounsand',store=True)
    coin_five_houndred_bundle = fields.Integer(string="Bundles")
    coin_five_houndred_count = fields.Integer(string="500 Coins")
    coin_five_houndred = fields.Monetary(string="500 Shs",compute='_compute_coin_five_houndred',store=True)
    coin_two_hundred_bundle = fields.Integer(string="Bundles")
    coin_two_hundred_count = fields.Integer(string="200 Coins")
    coin_two_hundred = fields.Monetary(string="200 Shs",compute='_compute_coin_two_hundred',store=True)
    coin_one_hundred_bundle = fields.Integer(string="Bundles")
    coin_one_hundred_count = fields.Integer(string="100 Coins")
    coin_one_hundred = fields.Monetary(string="100 Shs",compute='_compute_coin_one_hundred',store=True)
    coin_fifty_bundle = fields.Integer(string="Bundle")
    coin_fifty_count = fields.Integer(string="50 Coins")
    coin_fifty = fields.Monetary(string="50 Shs", compute='_compute_coin_fifty',store=True)
    
    sub_total_coins = fields.Monetary(compute='_compute_total_coins',string="Sub Total Coins",store=True,track_visibility='always')

    mutilated_coin_one_thounsand_bundle = fields.Integer(string="Bundles")
    mutilated_coin_one_thounsand_count = fields.Integer(string="1,000 Coins")
    mutilated_coin_one_thounsand = fields.Monetary(string="1,000 Shs", compute='_compute_coin_one_thounsand_mutilated',store=True)
    mutilated_coin_five_houndred_bundle = fields.Integer(string="Bundles")
    mutilated_coin_five_houndred_count = fields.Integer(string="500 Coins")
    mutilated_coin_five_houndred = fields.Monetary(string="500 Shs",compute='_compute_coin_five_houndred_mutilated',store=True)
    mutilated_coin_two_hundred_bundle = fields.Integer(string="Bundles")
    mutilated_coin_two_hundred_count = fields.Integer(string="200 Coins")
    mutilated_coin_two_hundred = fields.Monetary(string="200 Shs",compute='_compute_coin_two_hundred_mutilated',store=True)
    mutilated_coin_one_hundred_bundle = fields.Integer(string="Bundles")
    mutilated_coin_one_hundred_count = fields.Integer(string="100 Coins")
    mutilated_coin_one_hundred = fields.Monetary(string="100 Shs",compute='_compute_coin_one_hundred_mutilated',store=True)
    mutilated_coin_fifty_bundle = fields.Integer(string="Bundle")
    mutilated_coin_fifty_count = fields.Integer(string="50 Coins")
    mutilated_coin_fifty = fields.Monetary(string="50 Shs", compute='_compute_coin_fifty_mutilated',store=True)
    
    mutilated_sub_total_coins = fields.Monetary(compute='_compute_total_coins_mutilated',string="Sub Total Coins",store=True,track_visibility='always')

    mutilated_deno_fifty_thounsand_bundle = fields.Integer(string="Bundles")
    mutilated_deno_fifty_thounsand_count = fields.Integer(string="50,000 Loose Notes")
    mutilated_deno_fifty_thounsand = fields.Monetary(compute='_compute_deno_fifty_thounsand_mutilated_',string="50,000 Shs",store=True)
    mutilated_deno_twenty_thounsand_bundle = fields.Integer(string="Bundles")
    mutilated_deno_twenty_thounsand_count = fields.Integer(string="20,000 Loose Notes")
    mutilated_deno_twenty_thounsand = fields.Monetary(compute='_compute_deno_twenty_thounsand_mutilated_',string="20,000 Shs",store=True)
    mutilated_deno_ten_thounsand_bundle = fields.Integer(string="Bundles")
    mutilated_deno_ten_thounsand_count = fields.Integer(string="10,000 Loose Notes")
    mutilated_deno_ten_thounsand = fields.Monetary(string="10,000 Shs",compute='_compute_deno_ten_thounsand_mutilated_',store=True)
    mutilated_deno_five_thounsand_bundle = fields.Integer(string="Bundles")
    mutilated_deno_five_thounsand_count = fields.Integer(string="5,000 Loose  Notes")
    mutilated_deno_five_thounsand = fields.Monetary(string="5,000 Shs" ,compute='_compute_deno_five_thounsand_mutilated_',store=True)
    mutilated_deno_two_thounsand_bundle = fields.Integer(string="Bundles")
    mutilated_deno_two_thounsand_count = fields.Integer(string="2,000 Loose Notes")
    mutilated_deno_two_thounsand = fields.Monetary(string="2,000 Shs" ,compute='_compute_deno_two_thounsand_mutilated_',store=True)
    mutilated_deno_one_thounsand_bundle = fields.Integer(string="Bundles")
    mutilated_deno_one_thounsand_count = fields.Integer(string="1,000 Loose Notes")
    mutilated_deno_one_thounsand = fields.Monetary(string="1,000 Shs" ,compute='_compute_deno_one_thounsand_mutilated_',store=True)

    sub_total_mutilated = fields.Monetary(compute='_compute_total_mutilated_currency',string="Sub Total Mutilated",store=True,track_visibility='always')
    grand_total_ugx = fields.Monetary(compute='_compute_grand_totol',string="Grand Total (UGX)",store=True)
    system_cash_balance = fields.Monetary(string="System Cash Balance",required=True)
    shortage_cash = fields.Monetary(string="Shortage Cash",compute='_get_shortage',store=True)
    surplus_cash = fields.Monetary(string="Surplus Cash",compute='_get_surplus',store=True)
    created_on =  fields.Date(string='Date', default=lambda self: fields.Date.today())
    created_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    trx_proof = fields.Binary(string='Upload Teller Declaration', attachment=True,required=True)
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
            action_id = self.env.ref('spot_check.teller_list_action', raise_if_not_found=False)
            e.base_url = """{}/web#id={}&view_type=form&model=spot_check.teller&action={}""".format(web_base_url,e.id,action_id.id)

    @api.depends('mutilated_deno_fifty_thounsand_count','mutilated_deno_fifty_thounsand_bundle')
    def _compute_deno_fifty_thounsand_mutilated_(self):
        for record in self:
           record.mutilated_deno_fifty_thounsand = (record.mutilated_deno_fifty_thounsand_bundle * (100 * 50000)) + record.mutilated_deno_fifty_thounsand_count * 50000
    
    @api.depends('mutilated_deno_twenty_thounsand_count','mutilated_deno_twenty_thounsand_bundle')
    def _compute_deno_twenty_thounsand_mutilated_(self):
        for record in self:
           record.mutilated_deno_twenty_thounsand = (record.mutilated_deno_twenty_thounsand_bundle * (100 * 50000)) + record.mutilated_deno_twenty_thounsand_count * 20000

    @api.depends('mutilated_deno_ten_thounsand_count','mutilated_deno_ten_thounsand_bundle')
    def _compute_deno_ten_thounsand_mutilated_(self):
        for record in self:
           record.mutilated_deno_ten_thounsand = (record.mutilated_deno_five_thounsand_bundle * (100 * 1000)) + record.mutilated_deno_ten_thounsand_count * 10000

    @api.depends('mutilated_deno_five_thounsand_count','mutilated_deno_five_thounsand_bundle')
    def _compute_deno_five_thounsand_mutilated_(self):
        for record in self:
           record.mutilated_deno_five_thounsand = (record.mutilated_deno_five_thounsand_bundle * (100 * 5000)) + record.mutilated_deno_five_thounsand_count * 5000

    @api.depends('mutilated_deno_two_thounsand_count','mutilated_deno_two_thounsand_bundle')
    def _compute_deno_two_thounsand_mutilated_(self):
        for record in self:
           record.mutilated_deno_two_thounsand = (record.mutilated_deno_two_thounsand_bundle * (100 * 2000)) + record.mutilated_deno_two_thounsand_count * 2000

    @api.depends('mutilated_deno_one_thounsand_count','mutilated_deno_one_thounsand_bundle')
    def _compute_deno_one_thounsand_mutilated_(self):
        for record in self:
           record.mutilated_deno_one_thounsand = (record.mutilated_deno_one_thounsand_bundle * (100 * 1000))+ record.mutilated_deno_one_thounsand_count * 1000


    
    @api.depends('mutilated_coin_one_thounsand_count','mutilated_coin_one_thounsand_bundle')
    def _compute_coin_one_thounsand_mutilated(self):
        for record in self:
            record.mutilated_coin_one_thounsand = (record.mutilated_coin_one_thounsand_bundle * (1000 * 1000)) + record.mutilated_coin_one_thounsand_count * 1000
     
    @api.depends('mutilated_coin_five_houndred_count','mutilated_coin_five_houndred_bundle')
    def _compute_coin_five_houndred_mutilated(self):
        for record in self:
            record.mutilated_coin_five_houndred = (record.mutilated_coin_five_houndred_bundle * (1000 * 500)) + record.mutilated_coin_five_houndred_count * 500

    @api.depends('mutilated_coin_two_hundred_count','mutilated_coin_two_hundred_bundle')
    def _compute_coin_two_hundred_mutilated(self):
        for record in self:
            record.mutilated_coin_two_hundred = (record.mutilated_coin_two_hundred_bundle * (1000 * 200)) + record.mutilated_coin_two_hundred_count * 200

    
    @api.depends('mutilated_coin_one_hundred_count','mutilated_coin_one_hundred_bundle')
    def _compute_coin_one_hundred_mutilated(self):
        for record in self:
            record.mutilated_coin_one_hundred = (record.mutilated_coin_one_hundred_bundle * (1000 * 100)) + record.mutilated_coin_one_hundred_count *100

    @api.depends('mutilated_coin_fifty_count','mutilated_coin_fifty_bundle')
    def _compute_coin_fifty_mutilated(self):
        for record in self:
            record.mutilated_coin_fifty =(record.mutilated_coin_fifty_bundle * (1000 * 50))+ record.mutilated_coin_fifty_count *50

    
    @api.depends('coin_one_thounsand_count','coin_one_thounsand_bundle')
    def _compute_coin_one_thounsand(self):
        for record in self:
            record.coin_one_thounsand = (record.coin_one_thounsand_bundle * (1000 * 1000)) + record.coin_one_thounsand_count * 1000
     
    @api.depends('coin_five_houndred_count','coin_five_houndred_bundle')
    def _compute_coin_five_houndred(self):
        for record in self:
            record.coin_five_houndred = (record.coin_five_houndred_bundle * (1000 * 500)) + record.coin_five_houndred_count * 500

    @api.depends('coin_two_hundred_count','coin_two_hundred_bundle')
    def _compute_coin_two_hundred(self):
        for record in self:
            record.coin_two_hundred = (record.coin_two_hundred_bundle * (1000 * 200)) + record.coin_two_hundred_count * 200

    
    @api.depends('coin_one_hundred_count','coin_one_hundred_bundle')
    def _compute_coin_one_hundred(self):
        for record in self:
            record.coin_one_hundred = (record.coin_one_hundred_bundle * (1000 * 100)) + record.coin_one_hundred_count *100

    @api.depends('coin_fifty_count','coin_fifty_bundle')
    def _compute_coin_fifty(self):
        for record in self:
            record.coin_fifty =(record.coin_fifty_bundle * (1000 * 50))+ record.coin_fifty_count *50


    
    @api.depends('deno_fifty_thounsand_count','deno_fifty_thounsand_bundle')
    def _compute_deno_fifty_thounsand(self):
        for record in self:
           record.deno_fifty_thounsand = (record.deno_fifty_thounsand_bundle * (100 * 50000)) + record.deno_fifty_thounsand_count * 50000
    
    @api.depends('deno_twenty_thounsand_count','deno_twenty_thounsand_bundle')
    def _compute_deno_twenty_thounsand(self):
        for record in self:
           record.deno_twenty_thounsand = (record.deno_twenty_thounsand_bundle * (100 * 20000)) + record.deno_twenty_thounsand_count * 20000

    @api.depends('deno_ten_thounsand_count','deno_ten_thounsand_bundle')
    def _compute_deno_ten_thounsand(self):
        for record in self:
           record.deno_ten_thounsand = (record.deno_ten_thounsand_bundle * (100 * 10000)) + record.deno_ten_thounsand_count * 10000

    @api.depends('deno_five_thounsand_count','deno_five_thounsand_bundle')
    def _compute_deno_five_thounsand(self):
        for record in self:
           record.deno_five_thounsand = (record.deno_five_thounsand_bundle * (100 * 5000)) + record.deno_five_thounsand_count * 5000

    @api.depends('deno_two_thounsand_count','deno_two_thounsand_bundle')
    def _compute_deno_two_thounsand(self):
        for record in self:
           record.deno_two_thounsand = (record.deno_two_thounsand_bundle * (100 * 2000))+  record.deno_two_thounsand_count * 2000

    @api.depends('deno_one_thounsand_count','deno_one_thounsand_bundle')
    def _compute_deno_one_thounsand(self):
        for record in self:
           record.deno_one_thounsand = (record.deno_one_thounsand_bundle * (100 * 1000)) + record.deno_one_thounsand_count * 1000




    
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
    

    @api.depends('mutilated_coin_one_thounsand','mutilated_coin_five_houndred','mutilated_coin_two_hundred','mutilated_coin_one_hundred','mutilated_coin_fifty')
    def _compute_total_coins_mutilated(self):
        for record in self:
            record.mutilated_sub_total_coins =  record.mutilated_coin_one_thounsand + record.mutilated_coin_five_houndred + record.mutilated_coin_two_hundred + record.mutilated_coin_one_hundred + record.mutilated_coin_fifty


    @api.depends('sub_total_good', 'sub_total_coins','sub_total_mutilated','mutilated_sub_total_coins')
    def _compute_grand_totol(self):
        for record in self:
            record.grand_total_ugx = record.sub_total_good + record.sub_total_coins + record.sub_total_mutilated + record.mutilated_sub_total_coins 

    
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

    '''
    @api.depends('partner_id')    
    def _get_manager_id(self):
        if self.partner_id:
            self.branch_manager = self.partner_id.supervises
    '''
    @api.depends('teller_id')    
    def _get_till_id(self):
        if self.teller_id:
            self.till = self.teller_id.till_id
    '''
    @api.depends('branch_manager')    
    def _get_accountant_id(self):
        if self.branch_manager:
            self.branch_accountant = self.branch_manager.supervises  

    '''
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
        self.unique_field = (value or '')+''+(str(self.branch_code))+'-'+(str(date_time) or '')+'-'+(last or '')+''+(str(self.id))

    @api.one
    @api.constrains('system_cash_balance')
    def _check_system_cash_balance(self):
        if self.system_cash_balance <= 0.0:
            raise exceptions.ValidationError("Sorry, BR System Cash Balance Can Not Be {system_cash_balance} UGX. Please Fill In The Right Figures Before You Proceed. Contact Operations Department for assistance".format(system_cash_balance=self.system_cash_balance))
        
    
    @api.model
    def _update_notified_pending_confirmation_tellers(self):
        pending_conf = self.env['spot_check.teller'].search([('state', 'not in', ['reject_one','confirmed_one'])])
        for req in pending_conf:
            if req.state =='ongoing':
                template_id = self.env.ref('spot_check.email_template_create_teller_request').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(req.id,force_send=True)
    
    '''@api.one
    @api.constrains('branch_id')
    def _checkbranchspotcheck(self):
        pending_conf = self.env['spot_check.teller'].search([('state', 'in', ['ongoing'])])
        for res in pending_conf:
            if  res.branch_id.id == self.branch_id.id and res.state =='ongoing' and res.id is not self.id:
                raise exceptions.ValidationError(f"Hello {res.partner_id.name},  {res.branch_id.branch_name} still has a pending spot check confirmantion  of {res.grand_total_ugx:,.2f} UGX created on {res.created_on} by {res.created_by.name} . Kindly inform Teller {res.teller_id.name} to cosent all the spot checks before you proceed. For any more assistance please contact operations ")
    '''
    '''
    @api.one
    @api.constrains('created_on')
    def _checkbranchspotcheckToDay(self):
        pending_conf = self.env['spot_check.teller'].search([('state', 'in', ['ongoing','confirmed_one','reject_one'])])
        for res in pending_conf:
            if  res.created_on == self.created_on and res.branch_id.id == self.branch_id.id and res.id is not self.id:
                raise exceptions.ValidationError(f"Hello {res.partner_id.name},  {res.branch_id.branch_name} has already spot checked teller {res.teller_id.name} today of {res.created_on} by {res.created_by.name}. For any more assistance please contact operations cash section.")
      
    '''

    @api.model
    def _accountants_without_spotchecks(self):
        my_date = datetime.date.today() 
        week_num = my_date.isocalendar()
        branch_obj = self.env['spot_check.branch'].search([('status','in',['active'])])
        branch_list = []
        branch_list_done = []
        for i in branch_obj:
            branch_list.append(i.id)

        initiated_req = self.env['spot_check.teller'].search([('state', 'in', ['ongoing','confirmed_one','reject_one'])])
        for request in initiated_req:
            week_num_teller= request.created_on.isocalendar()
            if week_num != week_num_teller:
                branch_list_done.append(request.branch_id.id)
               

        branch_list_not_done = [x for x in branch_list if x not in branch_list_done]
        obj = self.env['res.partner'].search([('&'),('branch_id_spot_check','in',branch_list_not_done),('user_role','in',['accountant'])])

        for res in obj:
            template_id = self.env.ref('spot_check.email_template_accountants_teller_remiders').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(res.id,force_send=True)

    @api.model
    def _notfy_about_teller(self):
        my_date = datetime.date.today() # if date is 01/01/2018
        week_num = my_date.isocalendar()
        teller_obj = self.env['res.partner'].search([('user_role','in',['teller'])])

        teller_list = []
        teller_list_done = []
        for i in teller_obj:
            teller_list.append(i.id)

        initiated_req = self.env['spot_check.teller'].search([('state', 'in', ['ongoing','confirmed_one','reject_one'])])
        for request in initiated_req:
            week_num_teller= request.created_on.isocalendar()
            if week_num != week_num_teller:
                teller_list_done.append(request.teller_id.id)
               

        teller_list_not_done = [x for x in teller_list if x not in teller_list_done]
        obj = self.env['res.partner'].search([('&'),('id','in',teller_list_not_done),('user_role','in',['teller'])])

        for res in obj:
            template_id = self.env.ref('spot_check.email_template_accountants_teller_notfy').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(res.id,force_send=True)

    @api.model
    def _notfy_onetime_teller(self):
        my_date = datetime.date.today()
        week_num = my_date.isocalendar()
        teller_obj = self.env['res.partner'].search([('user_role','in',['teller'])])

        teller_list = []
        teller_list_done = []
        for i in teller_obj:
            teller_list.append(i.id)

        initiated_req = self.env['spot_check.teller'].search([('state', 'in', ['ongoing','confirmed_one','reject_one'])])
        for request in initiated_req:
            week_num_teller= request.created_on.isocalendar()
            if week_num == week_num_teller:
                teller_list_done.append(request.teller_id.id)
               

        teller_list_not_done = [x for x in teller_list if x  in teller_list_done]
       
        y = [z for z in teller_list_not_done if teller_list_not_done.count(z)==1]
        final_list = list(dict.fromkeys(y))
        obj = self.env['res.partner'].search([('&'),('id','in',final_list),('user_role','in',['teller'])])

        for result in obj:
            template_id = self.env.ref('spot_check.email_template_accountants_teller_notfy_penind').id
            template =  self.env['mail.template'].browse(template_id)
            template.send_mail(result.id,force_send=True)
         
