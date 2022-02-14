# -*- coding: utf-8 -*-
{
    'name': "Online Spot Check",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
    Onlie cash managment is a system that helps in day-to-day administration of managing cash inflows and outflows
    """,

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