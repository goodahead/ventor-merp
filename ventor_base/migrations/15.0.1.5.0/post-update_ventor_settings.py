from odoo import SUPERUSER_ID, _, api


def migrate(cr, version):

    env = api.Environment(cr, SUPERUSER_ID, {})

    group_settings = env["res.config.settings"].default_get(
        [
            "group_stock_production_lot",
            "group_stock_tracking_lot",
            "group_stock_tracking_owner"
        ]
    )

    if group_settings.get("group_stock_production_lot"):
        ventor_apply_default_lots = env['ventor.option.setting'].search(
            [
                ('technical_name', '=', 'apply_default_lots'),
            ]
        )
        ventor_apply_default_lots.is_readonly = False

    if group_settings.get("group_stock_tracking_lot"):
        ventor_apply_default_lots = env['ventor.option.setting'].search(
            [
                ('technical_name', '=', 'manage_packages'),
            ]
        )
        ventor_apply_default_lots. set_ventor_packages_fields(group_settings.get("group_stock_tracking_lot"))

    if group_settings.get("group_stock_tracking_owner"):
        ventor_apply_default_lots = env['ventor.option.setting'].search(
            [
                ('technical_name', '=', 'manage_product_owner'),
            ]
        )
        ventor_apply_default_lots.is_readonly = False
