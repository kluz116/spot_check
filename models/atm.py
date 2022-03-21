from odoo import models,api,fields

class ATM(models.Model):
    _name = "spot_check.atm"
    _inherit="mail.thread"
    _description = "This is an ATM model"
    _rec_name ="grand_total_ugx"
    
    partner_id = fields.Many2one ('res.partner', 'Customer', default = lambda self: self.env.user.partner_id )
    currency_id = fields.Many2one('res.currency', string='Currency' )

    state = fields.Selection([('ongoing', 'Pending Accountant Consent'),('confirmed_one', 'Pending Manager Consent'),('rejected_one', 'Rejected By Accountant'),('confirmed_two', 'Confirmed') ,('rejected_two', 'Rejected By Manager')],default="ongoing", string="Status",track_visibility='always')
    deno_fifty_thounsand = fields.Monetary(string="50,000 Shs")
    deno_twenty_thounsand = fields.Monetary(string="20,000 Shs")
    deno_ten_thounsand = fields.Monetary(string="10,000 Shs")
    deno_five_thounsand = fields.Monetary(string="5,000 Shs")
    deno_two_thounsand = fields.Monetary(string="2,000 Shs")
    deno_one_thounsand = fields.Monetary(string="1,000 Shs")
    sub_total_good = fields.Monetary(compute='_compute_total_good_currency',string="Sub Total Good Currency",store=True)
   
    grand_total_ugx = fields.Monetary(compute='_compute_grand_totol',string="Grand Total (UGX)",store=True,track_visibility='always')
    created_on =  fields.Datetime(string='Date', default=lambda self: fields.datetime.now())
    created_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    trx_proof = fields.Binary(string='Upload BRNET GL', attachment=True,required=True)
    trx_proof1 = fields.Binary(string='ATM Counters', attachment=True,required=True)
    trx_proof2 = fields.Binary(string='ATM Spot Recooncilations', attachment=True,required=True)
    branch_code = fields.Integer(compute='_compute_branch',string='Branch',store=True)
    branch_manager = fields.Many2one(compute='_get_manager_id', comodel_name='res.partner', string='Branch Manger', store=True)
    branch_accountant = fields.Many2one(compute='_get_accountant_id', comodel_name='res.partner', string='Branch Accountant', store=True)
    system_cash_balance = fields.Monetary(string="System Cash Balance",required=True)
    shortage_cash = fields.Monetary(string="Shortage Cash",compute='_get_shortage')
    surplus_cash = fields.Monetary(string="Surplus Cash",compute='_get_surplus')
    consent_status = fields.Char(string="Consent Status", compute='_get_consent')
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
        

    @api.depends('sub_total_good')
    def _compute_grand_totol(self):
        for record in self:
            record.grand_total_ugx = record.sub_total_good 

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

  
    
        
    