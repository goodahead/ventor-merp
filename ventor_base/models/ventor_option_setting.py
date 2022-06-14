# Copyright 2022 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import _, api, models, fields


class VentorOptionSetting(models.Model):
    _name = 'ventor.option.setting'
    _description = 'Ventor Option Setting'

    name = fields.Char(required=True, index=True)
    technical_name = fields.Char(required=True)
    value = fields.Many2one('ventor.setting.value', string='Value')
    setting_values = fields.One2many('ventor.setting.value', compute='_compute_setting_values')
    value_type = fields.Selection(
        [
            ('bool', 'Boolean'),
            ('select', 'Selection'),
        ]
    )
    action_type = fields.Selection(
        [
            ('warehouse_opration', 'Warehouse Opration'),
            ('package_management', 'Package Management'),
            ('batch_picking', 'Batch Picking'),
            ('internal_transfers', 'Internal Transfers'),
            ('putaway', 'Putaway'),
            ('instant_inventory', 'Instant Inventory'),
            ('inventory_adjustments', 'Inventory Adjustments'),
            ('quick_info', 'Quick Info'),
        ], required=True
    )
    description = fields.Text()

    @api.depends('value')
    def _compute_setting_values(self):
        for record in self:
            if record.value_type == 'bool':
                record.setting_values = self.env['ventor.setting.value'].search(
                    [
                        ('key', '=', record.value_type)
                    ]).ids
            elif record.value_type == 'select':
                record.setting_values = self.env['ventor.setting.value'].search(
                    [
                        ('key', '=', record.technical_name)
                    ]).ids
            else:
                record.setting_values = False

    def get_general_settings(self):
        action_types = [
            'package_management',
            'batch_picking',
            'internal_transfers',
            'putaway',
            'instant_inventory',
            'inventory_adjustments',
            'quick_info',
        ]
        ventor_option_settings = self.env['ventor.option.setting'].search([])
        settings = {}
        for action_type in action_types:
            settings[action_type] = {
                set.technical_name: self.set_value(set.value.value)
                for set in ventor_option_settings.filtered(lambda r: r.action_type == action_type)
            }
        return settings

    def set_value(self, value):
        if value.lower() == 'true':
            return True
        elif value.lower() == 'false':
            return False
        return value


class VentorSettingValue(models.Model):
    _name = 'ventor.setting.value'
    _description = 'Ventor Setting Value'
    _rec_name = 'value'

    key = fields.Char()
    value = fields.Char()
