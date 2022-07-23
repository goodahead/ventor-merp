# Copyright 2022 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import _, api, models, fields


class VentorOptionSetting(models.Model):
    _name = 'ventor.option.setting'
    _description = 'Ventor Option Setting'

    name = fields.Char(required=True, index=True)
    technical_name = fields.Char(required=True)
    value = fields.Many2one('ventor.setting.value', string='Value', required=True)
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
            ('cluster_picking', 'Cluster Picking'),
            ('internal_transfers', 'Internal Transfers'),
            ('putaway', 'Putaway'),
            ('instant_inventory', 'Instant Inventory'),
            ('inventory_adjustments', 'Inventory Adjustments'),
            ('quick_info', 'Quick Info'),
        ], required=True
    )
    description = fields.Text()
    settings_dependency = fields.Many2many(
        comodel_name='ventor.setting.value'
    )

    @api.onchange('value')
    def _onchange_value(self):
        if self.value.value == 'False' and self.technical_name == 'confirm_source_location':
            self.set_change_source_location()
        if self.value.value == 'False' and self.technical_name == 'manage_packages':
            self.set_related_package_fields()

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
            'cluster_picking',
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

    def set_change_source_location(self):
        change_source_location = self.env['ventor.option.setting'].search(
            [
                ('action_type', '=', self.action_type),
                ('technical_name', '=', 'change_source_location'),
            ]
        )
        if change_source_location.value.value == 'True':
            change_source_location.value = self.env.ref('ventor_base.bool_false').id

    def set_related_package_fields(self):
        confirm_source_package = self.env['ventor.option.setting'].search(
            [
                ('action_type', '=', self.action_type),
                ('technical_name', '=', 'confirm_source_package'),
            ]
        )
        scan_destination_package = self.env['ventor.option.setting'].search(
            [
                ('action_type', '=', self.action_type),
                ('technical_name', '=', 'scan_destination_package'),
            ]
        )
        confirm_source_package.value = scan_destination_package.value = self.env.ref('ventor_base.bool_false').id

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
