from odoo import SUPERUSER_ID, _, api


def migrate(cr, version):

    env = api.Environment(cr, SUPERUSER_ID, {})

    group_settings = env['res.config.settings'].default_get(
        [
            'group_stock_tracking_lot',
        ]
    )

    if group_settings.get('group_stock_tracking_lot'):
        putaway_manage_packages = env['ventor.option.setting'].search(
            [
                ('technical_name', '=', 'manage_packages'),
                ('action_type', '=', 'putaway'),
            ]
        )
        putaway_manage_packages.with_context(
            enable_putaway_manage_packages=True
        ).set_related_package_fields(group_settings.get('group_stock_tracking_lot'))
