from odoo import SUPERUSER_ID, _, api


def migrate(cr, version):

    env = api.Environment(cr, SUPERUSER_ID, {})
    group_stock_tracking_lot = (
            env["res.config.settings"]
            .default_get("group_stock_tracking_lot")
            .get("group_stock_tracking_lot")
    )
    stock_picking_type_ids = env['stock.picking.type'].with_context(active_test=False).search([])

    if not group_stock_tracking_lot:
        for stock_picking_type in stock_picking_type_ids:
            stock_picking_type.manage_packages = False

    elif group_stock_tracking_lot and not any(stock_picking_type_ids.mapped("manage_packages")):
        for stock_picking_type in stock_picking_type_ids:
            stock_picking_type.manage_packages = True
