from odoo import models,api,fields,exceptions

class ATM(models.Model):
    _name = "spot_check.atm"
    _inherit="mail.thread"
    _description = "This is an ATM model"
    _rec_name ="grand_total_ugx"
    
    partner_id = fields.Many2one ('res.partner', 'Customer', default = lambda self: self.env.user.partner_id )
    currency_id = fields.Many2one('res.currency', string='Currency',default=43 )

    branch_id = fields.Many2one('spot_check.branch',string ='Branch', required=True)
    #from_branch_id = fields.Integer(related='branch_id.id')
    branch_accountant = fields.Many2one('res.partner','Accountant',domain="[('branch_id_spot_check', '=', branch_id),('user_role','=','accountant')]")
    branch_manager = fields.Many2one('res.partner','Manager',domain="[('branch_id_spot_check', '=', branch_id),('user_role','=','manager')]")


    state = fields.Selection([('ongoing', 'Pending Accountant Consent'),('confirmed_one', 'Pending Manager Consent'),('rejected_one', 'Rejected By Accountant'),('confirmed_two', 'Confirmed') ,('rejected_two', 'Rejected By Manager')],default="ongoing", string="Status",track_visibility='always')
    deno_fifty_thounsand_bundle = fields.Integer(string="Bundles")
    deno_fifty_thounsand_count = fields.Integer(string="50,000 Loose Notes")
    deno_fifty_thounsand = fields.Monetary(compute='_compute_deno_fifty_thounsand',string="50,000 Shs",store=True)
    deno_twenty_thounsand_bundle = fields.Integer(string="Bundles")
    deno_twenty_thounsand_count = fields.Integer(string="20,000 Loose Notes")
    deno_twenty_thounsand = fields.Monetary(compute='_compute_deno_twenty_thounsand',string="20,000 Shs",store=True)
    deno_ten_thounsand_bundle = fields.Integer(string="Bundles")
    deno_ten_thounsand_count = fields.Integer(string="10,000 Loose Notes")
    deno_ten_thounsand = fields.Monetary(string="10,000 Shs",compute='_compute_deno_ten_thounsand',store=True)
    deno_five_thounsand_bundle = fields.Integer(string="Bundles")
    deno_five_thounsand_count = fields.Integer(string="5,000 Loose Notes")
    deno_five_thounsand = fields.Monetary(string="5,000 Shs" ,compute='_compute_deno_five_thounsand',store=True)
    sub_total_good = fields.Monetary(compute='_compute_total_good_currency',string="Sub Total Good Currency",store=True,track_visibility='always')
    
   
    grand_total_ugx = fields.Monetary(compute='_compute_grand_totol',string="Grand Total (UGX)",store=True,track_visibility='always')
    created_on =  fields.Date(string='Date', default=lambda self: fields.Date.today())
    created_by = fields.Many2one('res.users','Confirmed By:',default=lambda self: self.env.user)
    user_id = fields.Many2one('res.users', string='User', track_visibility='onchange', readonly=True, default=lambda self: self.env.user.id)
    trx_proof = fields.Binary(string='Upload BRNET GL', attachment=True,required=True)
    trx_proof1 = fields.Binary(string='ATM Counters', attachment=True,required=True)
    trx_proof2 = fields.Binary(string='ATM Spot Recooncilations', attachment=True,required=True)
    branch_code =  fields.Integer(related='branch_id.branch_code')
    #branch_manager = fields.Many2one(compute='_get_manager_id', comodel_name='res.partner', string='Branch Manger', store=True)
    #branch_accountant = fields.Many2one(compute='_get_accountant_id', comodel_name='res.partner', string='Branch Accountant', store=True)
    system_cash_balance = fields.Monetary(string="System Cash Balance",required=True)
    shortage_cash = fields.Monetary(string="Shortage Cash",compute='_get_shortage',store=True)
    surplus_cash = fields.Monetary(string="Surplus Cash",compute='_get_surplus',store=True)
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
            action_id = self.env.ref('spot_check.atm_list_action', raise_if_not_found=False)
            e.base_url = """{}/web#id={}&view_type=form&model=spot_check.atm&action={}""".format(web_base_url,e.id,action_id.id)


    
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




    @api.depends('deno_fifty_thounsand', 'deno_twenty_thounsand','deno_ten_thounsand','deno_five_thounsand')
    def _compute_total_good_currency(self):
        for record in self:
            record.sub_total_good = record.deno_fifty_thounsand + record.deno_twenty_thounsand + record.deno_ten_thounsand + record.deno_five_thounsand 
        

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
        
    
    

    @api.one
    @api.constrains('branch_id')
    def _checkbranchspotcheck(self):
        pending_conf = self.env['spot_check.atm'].search([('state', 'in', ['ongoing','confirmed_one'])])
        for res in pending_conf:
            if  res.branch_id.id == self.branch_id.id and res.state =='ongoing' and res.id is not self.id:
                raise exceptions.ValidationError(f"Hello {res.partner_id.name},  {res.branch_id.branch_name} still has a pending spot check confirmantion  of {res.grand_total_ugx:,.2f} UGX created on {res.created_on} by {res.created_by.name} . Kindly inform Accountant {res.branch_accountant.name} to cosent all the spot checks before you proceed. For any more assistance please contact operations ")
            elif res.branch_id.id == self.branch_id.id and res.state =='confirmed_one' and res.id is not self.id:
                raise exceptions.ValidationError(f"Hello {res.partner_id.name},  {res.branch_id.branch_name} still has a pending spot check confirmantion  of {res.grand_total_ugx:,.2f} UGX created on {res.created_on} by {res.created_by.name} . Kindly inform Manager {res.branch_manager.name} to cosent all the spot checks before you proceed. For any more assistance please contact operations ")
    @api.one
    @api.constrains('created_on')
    def _checkbranchspotcheckToDay(self):
        pending_conf = self.env['spot_check.atm'].search([('state', 'in', ['ongoing','confirmed_one','reject_one','confirmed_two'])])
        for res in pending_conf:
            if  res.created_on == self.created_on and res.branch_id.id == self.branch_id.id and res.id is not self.id:
                raise exceptions.ValidationError(f"Hello {res.partner_id.name},  {res.branch_id.branch_name} has already spot checked ATM today of {res.created_on} by {res.created_by.name}. For any more assistance please contact operations cash section.")
      
       
    @api.model
    def _update_notified_pending_confirmation_atm(self):
        pending_conf = self.env['spot_check.atm'].search([('state', 'in', ['ongoing','confirmed_one'])])
        for req in pending_conf:
            if req.state =='ongoing':
                template_id = self.env.ref('spot_check.email_template_create_atm_request').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(req.id,force_send=True)  
            elif  req.state =='confirmed_one':
                template_id = self.env.ref('spot_check.email_template_create_atm_request_to_manager').id
                template =  self.env['mail.template'].browse(template_id)
                template.send_mail(req.id,force_send=True)  