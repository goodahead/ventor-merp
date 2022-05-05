# Copyright 2022 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from . import models

from odoo import api, SUPERUSER_ID

def _post_init_hook(cr, registry):
    """
    This hook create and set WH Lot Name Sequence 
    for current warehouses
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    warehouses = env["stock.warehouse"].with_context(active_test=False).search([("lot_sequence_id", "=", False)])
    for wh in warehouses:
        if not wh.lot_sequence_id:
            lot_sequence_id = env["ir.sequence"].search([("code", "=", "stock.warehouse." + wh.code.lower())])
            if lot_sequence_id:
                wh.lot_sequence_id = lot_sequence_id
            else:
                wh._create_wh_lot_sequence()
