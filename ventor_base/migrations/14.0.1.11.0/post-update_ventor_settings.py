from odoo import SUPERUSER_ID, _, api


def migrate(cr, version):

    env = api.Environment(cr, SUPERUSER_ID, {})

    set_qty_to_zero = env.ref("ventor_base.set_qty_to_zero")
    if set_qty_to_zero:
        set_qty_to_zero.write(
            {
                "description": "Set all real quantity to zero",
            }
        )

    manage_packages_ins_inventory = env.ref("ventor_base.manage_packages_ins_inventory")
    if manage_packages_ins_inventory:
        manage_packages_ins_inventory.write(
            {
                "description": "It shows additional field 'Package' that you can scan to make an inventory in a package. "
                               "Works only if package management settings is active on Odoo side",
            }
        )
