# Odoo:
from odoo import SUPERUSER_ID, _, api


def migrate(cr, version):
    """Update warehouse_id for all stock inventory"""

    env = api.Environment(cr, SUPERUSER_ID, {})
    all_stock_inventory = env['stock.inventory'].search([
            ('state', 'in', ('draft', 'confirm', 'cancel', 'done')),
            ])
    for stock_inv in all_stock_inventory:
        warehouse_ids = stock_inv.location_ids.mapped("warehouse_id")
        if len(warehouse_ids) == 1:
            stock_inv.warehouse_id = warehouse_ids