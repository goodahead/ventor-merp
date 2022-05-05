# pylint: disable=missing-docstring
# Copyright 2022 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

{
    "name": "Yalla Stock Lot Number",
    "summary": "This module adds new logic to inventory application",
    "version": "14.0.1.0.0",
    "category": "Project Apps",
    "website": "https://ventor.tech/",
    "author": "VentorTech",
    "license": "LGPL-3",
    "depends": [
        "stock",
    ],
    "data": [
        "views/stock_warehouse_view.xml",
    ],
    "installable": True,
    "application": False,
    "post_init_hook": "_post_init_hook",
}
