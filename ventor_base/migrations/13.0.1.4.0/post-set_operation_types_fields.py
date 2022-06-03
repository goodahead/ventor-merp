from odoo import SUPERUSER_ID, _, api


def migrate(cr, version):

    env = api.Environment(cr, SUPERUSER_ID, {})
    group_stock_production_lot = (
            env["res.config.settings"]
            .default_get("group_stock_production_lot")
            .get("group_stock_production_lot")
    )
    stock_picking_type_ids = env['stock.picking.type'].with_context(active_test=False).search([])

    if not group_stock_production_lot:
        stock_picking_type_ids.apply_default_lots = False
