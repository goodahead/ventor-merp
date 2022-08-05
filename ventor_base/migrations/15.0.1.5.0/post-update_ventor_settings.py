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

    ventor_roles_administrator = env.ref('ventor_base.ventor_role_admin')
    ventor_roles_administrator.write(
        {
            'implied_ids': [(4, env.ref('ventor_base.merp_manage_ventor_configuration_app').id)],
        }
    )
