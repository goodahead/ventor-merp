from odoo import SUPERUSER_ID, _, api


def migrate(cr, version):

    env = api.Environment(cr, SUPERUSER_ID, {})

    # adding setting "Save transfer after exit"
    env["ventor.option.setting"].create(
        {
            "name": "Save transfer after exit",
            "technical_name": "save_transfer_after_exit",
            "value": env.ref("ventor_base.ask_me_every_time").id,
            "settings_dependency": [
                (4, env.ref('ventor_base.ask_me_every_time').id),
                (4, env.ref('ventor_base.save_transfer').id),
                (4, env.ref('ventor_base.cancel_transfer').id)
            ],
            "value_type": "select",
            "action_type": "internal_transfers",
            "description": "Choose the action on the transfer after exit the menu."
                           " You can save it or cancel without dialog screen"
        }
    )
