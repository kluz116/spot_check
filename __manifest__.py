# -*- coding: utf-8 -*-
{
    'name': "Online Spot Check",

    'summary': "This is a cash spot check application developed with Python Odoo Framework for ERPS",

    'description': "This is a cash spot check application developed with Python Odoo Framework for ERPS",
    'author': "Finance Trust Bank",
    'website': "http://www.financetrust.co.ug",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Finance',
    'version': '0.1',
    
    # any module necessary for this one to work correctly
    'depends': ['mail','base'],
  
    # always loaded
    'data': [
        'security/spot_check_security.xml',
        'security/ir.model.access.csv',
        'data/email_template_cash_managment.xml',
        'data/ir_cron_data.xml',
        'wizard/spot_check_vault_consent_accountant.xml',
        'wizard/spot_check_vault_consent_manager.xml',
        'wizard/spot_check_atm_consent_accountant.xml',
        'wizard/spot_check_atm_consent_manager.xml',
        'wizard/spot_check_consent_teller.xml',
        'wizard/spot_check_vault_reject_accountant.xml',
        'wizard/spot_check_vault_reject_manager.xml',
        'wizard/spot_check_atm_reject_accountant.xml',
        'wizard/spot_check_atm_reject_manager.xml',
        'wizard/spot_check_reject_teller.xml',
        'wizard/spot_check_vault_usd_consent_accountant.xml',
        'wizard/spot_check_vault_usd_consent_manager.xml',
        'wizard/spot_check_vault_usd_reject_accountant.xml',
        'wizard/spot_check_vault_usd_reject_manager.xml',
        'wizard/spot_check_reject_teller_usd.xml',
        'wizard/spot_check_consent_teller_usd.xml',
        'wizard/spot_check_mm_consent_teller.xml',
        'wizard/spot_check_mm_reject_teller.xml',
        'views/branch.xml',
        'views/spot_check.xml',
        'views/spots_user.xml',
        'views/reports.xml',
        'reports/report_spot.xml',
        'reports/report_vault.xml',
        'reports/report_atm.xml',
        'reports/report_teller.xml',
        'reports/confirmed_reports.xml',
        'reports/ongoing_report.xml'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}