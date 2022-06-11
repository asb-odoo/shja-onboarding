{
    'name': 'Sale Management',
    'version': '15.0.1.0.0',
    'description': """This Module is used for adding second discount field in 
                                sale module and as well as made changes in different reports like sale_report,account_report 
                                    etc """,
    'category':'sale',
    'license': 'LGPL-3',
    'depends': ['sale_management'],
    'data': [
        'views/sale_order_view.xml',
        'views/account_move_view.xml',
        'report/sale_report_templates_inherit.xml',
        'report/report_invoice_inherit.xml',
        ],
    'installable': True,
    'auto_install': False,
}
