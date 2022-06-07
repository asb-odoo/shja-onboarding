{
    'name': 'Sale Management',
    'version': '1.0.0',
    'description': """This Module is used for extend functionality of existing module""",
    'category':'sale',
    'license': 'LGPL-3',
    'depends': ['sale_management','account'],
    'data': [
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'report/sale_report_templates_inherit.xml',
        'report/report_invoice_inherit.xml',
        ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
