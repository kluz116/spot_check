from odoo import models, fields, api,tools

class ReportingSummary(models.Model):
    _name = "spot_check.reportsummary"
    _auto = False
    _order = "spot_month asc"

    branch_id = fields.Many2one('spot_check.branch',string ='Branch')
    count = fields.Integer(string="Coumt(Number of spot checks)")
    spot_month = fields.Char(string='Month')
    spot_year = fields.Integer(string='Year')
    spot_check_type = fields.Char(string='Type')


    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, 'spot_check_reportsummary')
        self._cr.execute(""" CREATE OR REPLACE VIEW spot_check_reportsummary AS(
              select row_number() OVER (ORDER BY 1) AS id,* from (
                SELECT a.branch_id,
                count(*),
                CASE
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='1' THEN 'Jan'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='2' THEN 'Feb'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='3' THEN 'Mar'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='4' THEN 'Apr' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='5' THEN 'May' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='6' THEN 'June' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='7' THEN 'July'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='8' THEN 'Aug'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='9' THEN 'Sept'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='10' THEN 'Oct'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='11' THEN 'Nov'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='12' THEN 'Dec'
                END AS Spot_month,
                EXTRACT(YEAR FROM CAST(a.created_on AS DATE)) AS Spot_year,
                'Teller Spot Check - UGX' AS spot_check_type
                FROM public.spot_check_teller a  where a.state not in ('ongoing','rejected_one')  group by a.branch_id,EXTRACT(MONTH FROM CAST(a.created_on AS DATE)),EXTRACT(YEAR FROM CAST(a.created_on AS DATE)) 
                
                UNION ALL 
                SELECT a.branch_id,
                count(*),
                CASE
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='1' THEN 'Jan'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='2' THEN 'Feb'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='3' THEN 'Mar'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='4' THEN 'Apr' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='5' THEN 'May' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='6' THEN 'June' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='7' THEN 'July'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='8' THEN 'Aug'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='9' THEN 'Sept'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='10' THEN 'Oct'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='11' THEN 'Nov'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='12' THEN 'Dec'
                END AS Spot_month,
                EXTRACT(YEAR FROM CAST(a.created_on AS DATE)) AS Spot_year,
                'Teller Spot Check - USD' AS spot_check_type
                FROM public.spot_check_teller_usd a  where a.state not in ('ongoing','rejected_one') group by a.branch_id,EXTRACT(MONTH FROM CAST(a.created_on AS DATE)),EXTRACT(YEAR FROM CAST(a.created_on AS DATE))
                
                UNION ALL 
                SELECT a.branch_id,
                count(*),
                CASE
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='1' THEN 'Jan'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='2' THEN 'Feb'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='3' THEN 'Mar'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='4' THEN 'Apr' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='5' THEN 'May' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='6' THEN 'June' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='7' THEN 'July'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='8' THEN 'Aug'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='9' THEN 'Sept'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='10' THEN 'Oct'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='11' THEN 'Nov'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='12' THEN 'Dec'
                END AS Spot_month,
                EXTRACT(YEAR FROM CAST(a.created_on AS DATE)) AS Spot_year,
                'Vault Spot Check - USD' AS spot_check_type
                FROM public.spot_check_vault_usd a  where a.state not in ('ongoing','rejected_one') group by a.branch_id,EXTRACT(MONTH FROM CAST(a.created_on AS DATE)),EXTRACT(YEAR FROM CAST(a.created_on AS DATE))
                
                UNION ALL 
                SELECT a.branch_id,
                count(*),
                CASE
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='1' THEN 'Jan'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='2' THEN 'Feb'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='3' THEN 'Mar'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='4' THEN 'Apr' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='5' THEN 'May' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='6' THEN 'June' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='7' THEN 'July'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='8' THEN 'Aug'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='9' THEN 'Sept'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='10' THEN 'Oct'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='11' THEN 'Nov'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='12' THEN 'Dec'
                END AS Spot_month,
                EXTRACT(YEAR FROM CAST(a.created_on AS DATE)) AS Spot_year,
                'Vault Spot Check - UGX' AS spot_check_type
                FROM public.spot_check_vault a  where a.state not in ('ongoing','rejected_one')  group by a.branch_id,EXTRACT(MONTH FROM CAST(a.created_on AS DATE)),EXTRACT(YEAR FROM CAST(a.created_on AS DATE))
                
                    UNION ALL 
                SELECT a.branch_id,
                count(*),
                CASE
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='1' THEN 'Jan'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='2' THEN 'Feb'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='3' THEN 'Mar'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='4' THEN 'Apr' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='5' THEN 'May' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='6' THEN 'June' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='7' THEN 'July'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='8' THEN 'Aug'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='9' THEN 'Sept'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='10' THEN 'Oct'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='11' THEN 'Nov'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='12' THEN 'Dec'
                END AS Spot_month,
                EXTRACT(YEAR FROM CAST(a.created_on AS DATE)) AS Spot_year,
                'ATM Spot Check - UGX' AS spot_check_type
                FROM public.spot_check_atm a  where a.state not in ('ongoing','rejected_one')  group by a.branch_id,EXTRACT(MONTH FROM CAST(a.created_on AS DATE)),EXTRACT(YEAR FROM CAST(a.created_on AS DATE))
                
                    UNION ALL 
                SELECT a.branch_id,
                count(*),
                CASE
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='1' THEN 'Jan'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='2' THEN 'Feb'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='3' THEN 'Mar'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='4' THEN 'Apr' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='5' THEN 'May' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='6' THEN 'June' 
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='7' THEN 'July'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='8' THEN 'Aug'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='9' THEN 'Sept'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='10' THEN 'Oct'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='11' THEN 'Nov'
                WHEN EXTRACT(MONTH FROM CAST(a.created_on AS DATE)) ='12' THEN 'Dec'
                END AS Spot_month,
                EXTRACT(YEAR FROM CAST(a.created_on AS DATE)) AS Spot_year,
                'Mobile Money Spot Check - UGX' AS spot_check_type
                FROM public.spot_check_mobile_money a  where a.state not in ('ongoing','rejected_one')  group by a.branch_id,EXTRACT(MONTH FROM CAST(a.created_on AS DATE)),EXTRACT(YEAR FROM CAST(a.created_on AS DATE))
                ) AS b order by b.Spot_month asc)""")







  
