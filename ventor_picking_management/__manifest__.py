# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

{
    'name': 'Picking management PRO',
    'summary': '',
    'version': '14.0.1.0.0',
    'category': 'Tools',
    'website': 'https://ventor.tech/',
    'author': 'VentorTech',
    'images': ['static/description/icon.png'],
    'license': 'LGPL-3',
    'depends': [
        # 'ventor_base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_batch_rule_view.xml',
    ],
    'installable': True,
}
# {
#     'name': 'Picking management PRO',
#     'version': '14.0.1.3.8',
#     'author': 'VentorTech',
#     'website': 'https://ventor.tech/',
#     'license': 'LGPL-3',
#     'installable': True,
#     # 'images': ['static/description/main_banner.png'],
#     'summary': 'Base module that allow relation between Ventor modules',
#     'depends': [
#         'ventor_base',
#     ],
#     'data': [
#     ],
# }