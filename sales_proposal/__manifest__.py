{
    'name': 'Sales Proposal',
    'version': '15.0.1.0.0',
    'summary':'sale_proposal',
    'description': """This module is used to manage the proposal of products to the
                                customer """,
    'category':'sale',
    'license': 'LGPL-3',
    'depends': ['sale_management'],
    'data': [
        'data/ir_sequence_data.xml',
        'views/sale_views.xml',
        ],
    'installable': True,
}
