# Copyright 2022 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import _, api, models, fields


class VentorOptionSetting(models.Model):
    _name = 'ventor.option.setting'
    _description = 'Ventor Option Setting'

    name = fields.Char(required=True, index=True)
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
    is_readonly = fields.Boolean(default=False, readonly=True)
    technical_name = fields.Char(required=True)
    value = fields.Many2one('ventor.setting.value', string='Value', required=True)
    value_type = fields.Selection(
        [
            ('bool', 'Boolean'),
            ('select', 'Selection'),
        ]
    )
    settings_dependency = fields.Many2many(
        comodel_name='ventor.setting.value'
    )

    @api.onchange('value')
    def _onchange_value(self):
        if self.technical_name == 'confirm_source_location':
            self._set_change_source_location()
        if self.technical_name == 'manage_packages':
            self._set_related_package_fields()
        if self.technical_name == 'add_boxes_before_cluster':
            self._set_add_boxes_before_cluster()

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
                set.technical_name: self.set_value(set.value.setting_value)
                for set in ventor_option_settings.filtered(lambda r: r.action_type == action_type)
            }
        return settings

    def _set_add_boxes_before_cluster(self):
        multiple_boxes_for_one_transfer = self.env['ventor.option.setting'].search(
            [
                ('action_type', '=', self.action_type),
                ('technical_name', '=', 'multiple_boxes_for_one_transfer'),
            ]
        )
        if self.value.setting_value == 'True':
            multiple_boxes_for_one_transfer.is_readonly = True
            multiple_boxes_for_one_transfer.value = self.env.ref('ventor_base.bool_false')
        else:
            multiple_boxes_for_one_transfer.is_readonly = False
            
    def _set_change_source_location(self):
        change_source_location = self.env['ventor.option.setting'].search(
            [
                ('action_type', '=', self.action_type),
                ('technical_name', '=', 'change_source_location'),
            ]
        )
        if self.value.setting_value == 'True':
            change_source_location.is_readonly = False
        else:
            change_source_location.value = self.env.ref('ventor_base.bool_false')
            change_source_location.is_readonly = True

    def _set_related_package_fields(self):
        for item in self:
            confirm_source_package = self.env['ventor.option.setting'].search(
                [
                    ('action_type', '=', item.action_type),
                    ('technical_name', '=', 'confirm_source_package'),
                ]
            )
            scan_destination_package = self.env['ventor.option.setting'].search(
                [
                    ('action_type', '=', item.action_type),
                    ('technical_name', '=', 'scan_destination_package'),
                ]
            )
            if item.value.setting_value == 'True':
                confirm_source_package.is_readonly = scan_destination_package.is_readonly = False
            else:
                confirm_source_package.value = scan_destination_package.value = self.env.ref('ventor_base.bool_false')
                confirm_source_package.is_readonly = scan_destination_package.is_readonly = True

    def set_ventor_packages_fields(self, group_stock_tracking_lot):
        self.is_readonly = not group_stock_tracking_lot
        if not group_stock_tracking_lot:
            self.value = self.env.ref('ventor_base.bool_false')
            self.filtered(
                lambda x: x.action_type in ('batch_picking', 'cluster_picking')
            )._set_related_package_fields()
        else:
            self.filtered(lambda x: x.action_type == 'putaway').value = self.env.ref('ventor_base.bool_true')
            self.filtered(lambda x: x.action_type in ('batch_picking', 'cluster_picking'))._set_related_package_fields()

    def set_value(self, setting_value):
        if setting_value.lower() == 'true':
            return True
        elif setting_value.lower() == 'false':
            return False
        return setting_value


class VentorSettingValue(models.Model):
    _name = 'ventor.setting.value'
    _description = 'Ventor Setting Value'
    _rec_name = 'setting_value'

    setting_type = fields.Char()
    setting_value = fields.Char()
