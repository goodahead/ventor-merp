from odoo import SUPERUSER_ID, _, api


def migrate(cr, version):

    env = api.Environment(cr, SUPERUSER_ID, {})

    allow_validate_less = env.ref("ventor_base.allow_validate_less")
    allow_validate_less.write(
        {
            "name": "Validate uncompleted orders",
            "description": "Validate uncompleted orders“, new description “User will be able to validate the order even if not all items were found"
        }
    )
