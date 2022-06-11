from odoo import models, fields, api,tools
from datetime import datetime

class Reporting(models.Model):
    _name = "spot_check.report"
    _auto = False
    _rec_name ="created_on"
    _order = "created_on desc"

    currency_id = fields.Many2one('res.currency', string='Currency')
    branch_id = fields.Many2one('spot_check.branch',string ='Branch')
    branch_accountant = fields.Many2one('res.partner','Accountant')
    branch_manager = fields.Many2one('res.partner','Manager')
    state = fields.Char(string='Status')
    sub_total_good = fields.Monetary(string="Total Cash")
    sub_total_coins = fields.Monetary(string="Total Coins")
    sub_total_mutilated = fields.Monetary(string="Total Mutilated")
    mutilated_sub_total_coins = fields.Monetary(string="Total Mutilated Coins")
    grand_total_ugx = fields.Monetary(string="Grand Total")
    system_cash_balance = fields.Monetary(string="System Cash Balance")
    shortage_cash = fields.Monetary(string="Shortage Cash")
    surplus_cash = fields.Monetary(string="Surplus Cash")
    created_on = fields.Date(string='Date')
    created_by = fields.Many2one('res.users','Created By')
    spot_check_type = fields.Char(string='Type')


    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'spot_check_report')
        self._cr.execute(""" CREATE OR REPLACE VIEW spot_check_report AS(
            
                select row_number() OVER (ORDER BY 1) AS id,* from (
                 SELECT a.currency_id, a.branch_id,
                a.branch_accountant, a.branch_manager, a.state,a.sub_total_good, a.sub_total_coins, a.sub_total_mutilated,a.mutilated_sub_total_coins, a.grand_total_ugx,  a.system_cash_balance,a.shortage_cash, a.surplus_cash, CAST(a.created_on AS DATE) AS created_on, a.created_by,'Vault Spot Check' AS spot_check_type
                FROM public.spot_check_vault a 

                UNION ALL

                SELECT  a.currency_id, a.branch_id,
                a.branch_accountant, a.branch_manager, a.state,a.sub_total_good, 0 AS sub_total_coins, a.sub_total_mutilated, 0 AS mutilated_sub_total_coins, a.grand_total_ugx,  a.system_cash_balance,a.shortage_cash, a.surplus_cash,CAST(a.created_on AS DATE) AS created_on, a.created_by,'Vault Spot Check' AS spot_check_type
                FROM public.spot_check_vault_usd a 
                
                UNION ALL
                
                 SELECT a.currency_id, a.branch_id,
                a.branch_accountant, a.branch_manager, a.state,a.sub_total_good, a.sub_total_coins, a.sub_total_mutilated,a.mutilated_sub_total_coins, a.grand_total_ugx,  a.system_cash_balance,a.shortage_cash, a.surplus_cash, CAST(a.created_on AS DATE) AS created_on, a.created_by,'Teller Spot Check' AS spot_check_type
                FROM public.spot_check_teller a 

                UNION ALL

                SELECT  a.currency_id, a.branch_id,
                a.branch_accountant, a.branch_manager, a.state,a.sub_total_good, 0 AS sub_total_coins, a.sub_total_mutilated, 0 AS mutilated_sub_total_coins, a.grand_total_ugx,  a.system_cash_balance,a.shortage_cash, a.surplus_cash,CAST(a.created_on AS DATE) AS created_on, a.created_by,'Teller Spot Check' AS spot_check_type
                FROM public.spot_check_teller_usd a 

                UNION ALL

                SELECT  a.currency_id, a.branch_id,
                a.branch_accountant, a.branch_manager, a.state,a.sub_total_good, 0 AS sub_total_coins, 0 AS sub_total_mutilated, 0 AS mutilated_sub_total_coins, a.grand_total_ugx,  a.system_cash_balance,a.shortage_cash, a.surplus_cash,CAST(a.created_on AS DATE) AS created_on, a.created_by,'ATM Spot Check' AS spot_check_type
                FROM public.spot_check_atm a 

                UNION ALL

                SELECT  a.currency_id, a.branch_id,
                a.branch_accountant, a.branch_manager, a.state,0 AS sub_total_good, 0 AS sub_total_coins, 0 AS sub_total_mutilated, 0 AS mutilated_sub_total_coins, a.grand_total_ugx,  a.system_cash_balance,a.shortage_cash, a.surplus_cash,CAST(a.created_on AS DATE) AS created_on, a.created_by,'Mobile Money Spot Check' AS spot_check_type
                FROM public.spot_check_mobile_money a 
                ) AS x where x.state not in ('ongoing','rejected_one') order by x.created_on desc)""")







  
