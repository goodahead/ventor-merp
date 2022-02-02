from odoo import SUPERUSER_ID, _, api


def migrate(cr, version):

    env = api.Environment(cr, SUPERUSER_ID, {})
    group_stock_tracking_lot = (
            env["res.config.settings"]
            .default_get("group_stock_tracking_lot")
            .get("group_stock_tracking_lot")
    )
    if group_stock_tracking_lot:
        for stock_picking_type in env['stock.picking.type'].with_context(active_test=False).search([]):
            stock_picking_type.manage_packages = True
