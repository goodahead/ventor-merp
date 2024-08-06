from odoo import SUPERUSER_ID, _, api


def migrate(cr, version):

    env = api.Environment(cr, SUPERUSER_ID, {})

    prohibition_on_updating_inventory = env.ref(
        'ventor_base.prohibition_on_updating_inventory',
        False,
    )

    if prohibition_on_updating_inventory:
        prohibition_on_updating_inventory.write(
            {
                'name': 'Hide update inventory button',
            }
        )
