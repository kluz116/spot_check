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
        'wizard/spot_check_vault_consent_accountant.xml',
        'wizard/spot_check_vault_consent_manager.xml',
        'wizard/spot_check_atm_consent_accountant.xml',
        'wizard/spot_check_atm_consent_manager.xml',
        'views/branch.xml',
        'views/spot_check.xml',
        'views/spots_user.xml'
        #'reports/cash_bank_request_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}