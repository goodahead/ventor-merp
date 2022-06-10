# Copyright 2022 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import models, fields


class VentorOptionSetting(models.Model):
    _name = 'ventor.option.setting'
    _description = 'Ventor Option Setting'

    name = fields.Char(required=True, index=True)
    technical_name = fields.Char(required=True)
    is_set = fields.Boolean()
    action_type = fields.Selection(
        [
            ('warehouse_opration', 'Warehouse Opration'),
            ('package_management', 'Package Management'),
            ('batch_picking', 'Batch Picking'),
            ('internal_transfers', 'Internal Transfers'),
            ('putaway', 'Putaway'),
            ('instant_inventory', 'Instant Inventory'),
            ('inventory_adjustments', 'Inventory Adjustments'),
            ('quick_info', 'quick_info'),
        ], required=True
    )
    description = fields.Text()

    def get_general_settings(self):
        action_types = [
            'package_management', 
            'batch_picking',
            'internal_transfers',
            'putaway',
            'instant_inventory',
            'inventory_adjustments',
            'quick_info'
        ]
        ventor_option_settings = self.env['ventor.option.setting'].search([])
        settings = {}
        for action_type in action_types:
            settings[action_type] = {
                set.technical_name: set.is_set
                for set in ventor_option_settings.filtered(lambda r: r.action_type == action_type)
            }
        return settings
