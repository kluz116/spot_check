from odoo import models,api,fields,exceptions

class TellersUsd(models.Model):
    _name = "spot_check.teller_usd"
    _inherit="mail.thread"
    _description = "This is a a tellers model"
    _rec_name ="grand_total_ugx"
    
    partner_id = fields.Many2one ('res.partner', 'Accountant', default = lambda self: self.env.user.partner_id )
    from_branch_id = fields.Integer(related='partner_id.branch_id_spot_check.id')
    currency_id = fields.Many2one('res.currency', string='Currency',default=2  )
    branch_id = fields.Many2one('spot_check.branch',string ='Branch',default = lambda self:self.from_branch_id ,required=True)
    teller_id = fields.Many2one('res.partner','Teller',domain="[('branch_id_spot_check', '=', branch_id),('user_role','=','teller')]")
    till = fields.Char(string='Till ID',compute='_get_till_id')
    state = fields.Selection([('ongoing', 'Pending Teller Consent'),('confirmed_one', 'Confirmed'),('reject_one', 'Rejected By Teller')],default="ongoing", string="Status")
    
    hundred_dollar_bundle = fields.Integer(string="Bundles")
    hundred_dollar_count = fields.Integer(string="100 Notes")
    hundred_dollar = fields.Monetary(string="$100", compute='_compute_hundred_dollar')
    fifty_dollar_bundle = fields.Integer(string="Bundles")
    fifty_dollar_count = fields.Integer(string="50 Notes")
    fifty_dollar = fields.Monetary(string="$50",compute='_compute_fifty_dollar')
    twenty_dollar_bundle = fields.Integer(string="Bundles")
    twenty_dollar_count = fields.Integer(string="20 Notes")
    twenty_dollar = fields.Monetary(string="$20",compute='_compute_twenty_dollar')
    ten_dollar_bundle = fields.Integer(string="Bundles")
    ten_dollar_count = fields.Integer(string="10 Notes")
    ten_dollar = fields.Monetary(string="$10",compute='_compute_ten_dollar')
    five_dollar_bundle = fields.Integer(string="Bundles")
    five_dollar_count = fields.Integer(string="5 Notes")
    five_dollar = fields.Monetary(string="$5",compute='_compute_five_dollar')
    one_dollar_bundle = fields.Integer(string="Bundles")
    one_dollar_count = fields.Integer(string="1 Notes")
    one_dollar = fields.Monetary(string="$1",compute='_compute_one_dollar')
    sub_total_good = fields.Monetary(compute='_compute_total_good_currency',string="Sub Total Good Currency",store=True,track_visibility='always')
    mutilated_hundred_dollar_bundle = fields.Integer(string="Bundles")
    mutilated_hundred_dollar_count = fields.Integer(string="100 Notes")
    mutilated_hundred_dollar = fields.Monetary(string="$100", compute='_compute_mutilated_hundred_dollar')
    mutilated_fifty_dollar_bundle = fields.Integer(string="Bundles")
    mutilated_fifty_dollar_count = fields.Integer(string="50 Notes")
    mutilated_fifty_dollar = fields.Monetary(string="$50",compute='_compute_mutilated_fifty_dollar')
    mutilated_twenty_dollar_bundle = fields.Integer(string="Bundles")
    mutilated_twenty_dollar_count = fields.Integer(string="20 Notes")
    mutilated_twenty_dollar = fields.Monetary(string="$20",compute='_compute_mutilated_twenty_dollar')
    mutilated_ten_dollar_bundle = fields.Integer(string="Bundles")
    mutilated_ten_dollar_count = fields.Integer(string="10 Notes")
    mutilated_ten_dollar = fields.Monetary(string="$10",compute='_compute_mutilated_ten_dollar')
    mutilated_five_dollar_bundle = fields.Integer(string="Bundles")
    mutilated_five_dollar_count = fields.Integer(string="5 Notes")
    mutilated_five_dollar = fields.Monetary(string="$5",compute='_compute_mutilated_five_dollar')
    mutilated_one_dollar_bundle = fields.Integer(string="Bundles")
    mutilated_one_dollar_count = fields.Integer(string="1 Notes")
    mutilated_one_dollar = fields.Monetary(string="$1",compute='_compute_mutilated_one_dollar')

    sub_total_mutilated = fields.Monetary(compute='_compute_total_mutilated_currency',string="Sub Total Mutilated",store=True,track_visibility='always')
    grand_total_ugx = fields.Monetary(compute='_compute_grand_totol',string="Grand Total (USD)",store=True)
    system_cash_balance = fields.Monetary(string="System Cash Balance")
    shortage_cash = fields.Monetary(string="Shortage Cash",compute='_get_shortage',store=True)
    surplus_cash = fields.Monetary(string="Surplus Cash",compute='_get_surplus',store=True)
    created_on =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
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
            action_id = self.env.ref('spot_check.teller_list_action_usd', raise_if_not_found=False)
            e.base_url = """{}/web#id={}&view_type=form&model=spot_check.teller_usd&action={}""".format(web_base_url,e.id,action_id.id)


    @api.depends('mutilated_hundred_dollar_count','mutilated_hundred_dollar_bundle')
    def _compute_mutilated_hundred_dollar(self):
        for record in self:
           record.mutilated_hundred_dollar = (record.mutilated_hundred_dollar_bundle * (100 * 100)) + record.mutilated_hundred_dollar_count * 100

    @api.depends('mutilated_fifty_dollar_count','mutilated_fifty_dollar_bundle')
    def _compute_mutilated_fifty_dollar(self):
        for record in self:
           record.mutilated_fifty_dollar = (record.mutilated_fifty_dollar_bundle * (50 * 100)) + record.mutilated_fifty_dollar_count * 50

    @api.depends('mutilated_twenty_dollar_count','mutilated_twenty_dollar_bundle')
    def _compute_mutilated_twenty_dollar(self):
        for record in self:
           record.mutilated_twenty_dollar = (record.mutilated_twenty_dollar_bundle * (20 * 100)) + record.mutilated_twenty_dollar_count * 20

    @api.depends('mutilated_ten_dollar_count','mutilated_ten_dollar_bundle')
    def _compute_mutilated_ten_dollar(self):
        for record in self:
           record.mutilated_ten_dollar = (record.mutilated_ten_dollar_bundle * (10 * 100))  + record.mutilated_ten_dollar_count * 10

    @api.depends('mutilated_five_dollar_count','mutilated_five_dollar_bundle')
    def _compute_mutilated_five_dollar(self):
        for record in self:
           record.mutilated_five_dollar = (record.mutilated_five_dollar_bundle * (10 * 100)) + record.mutilated_five_dollar_count * 5

    @api.depends('mutilated_one_dollar_count','mutilated_one_dollar_bundle')
    def _compute_mutilated_one_dollar(self):
        for record in self:
           record.mutilated_one_dollar = (record.mutilated_one_dollar_bundle * (1 * 100)) + record.mutilated_one_dollar_count * 1

    @api.depends('hundred_dollar_count','hundred_dollar_bundle')
    def _compute_hundred_dollar(self):
        for record in self:
           record.hundred_dollar = (record.hundred_dollar_bundle * (100 * 100))+ record.hundred_dollar_count * 100

    @api.depends('fifty_dollar_count','fifty_dollar_bundle')
    def _compute_fifty_dollar(self):
        for record in self:
           record.fifty_dollar = (record.fifty_dollar_bundle * (50 * 100)) + record.fifty_dollar_count * 50

    @api.depends('twenty_dollar_count','twenty_dollar_bundle')
    def _compute_twenty_dollar(self):
        for record in self:
           record.twenty_dollar = (record.twenty_dollar_bundle * (20 * 100)) +record.twenty_dollar_count * 20

    @api.depends('ten_dollar_count','ten_dollar_bundle')
    def _compute_ten_dollar(self):
        for record in self:
           record.ten_dollar = (record.ten_dollar_bundle * (10 * 100)) + record.ten_dollar_count * 10

    @api.depends('five_dollar_count','five_dollar_bundle')
    def _compute_five_dollar(self):
        for record in self:
           record.five_dollar = (record.five_dollar_bundle * (5 * 100)) + record.five_dollar_count * 5

    @api.depends('one_dollar_count','one_dollar_bundle')
    def _compute_one_dollar(self):
        for record in self:
           record.one_dollar = (record.one_dollar_bundle * (1 * 100)) + record.one_dollar_count * 1




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
    
    @api.one
    @api.constrains('system_cash_balance')
    def _check_system_cash_balance(self):
        if self.system_cash_balance <= 0.0:
            raise exceptions.ValidationError("Sorry, BR System Cash Balance Can Not Be {system_cash_balance} USD. Please Fill In The Right Figures Before You Proceed. Contact Operations Department for assistance".format(system_cash_balance=self.system_cash_balance))


    @api.model
    def _update_notified_pending_confirmation_tellers_usd(self):
        pending_conf = self.env['spot_check.teller_usd'].search([('state', 'not in', ['reject_one','confirmed_one'])])
        for req in pending_conf:
            if req.state =='ongoing':
                template_id = self.env.ref('spot_check.email_template_create_teller_request_usd').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(req.id,force_send=True)

            