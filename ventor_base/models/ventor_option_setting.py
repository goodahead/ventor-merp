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
        if self.technical_name in ('confirm_source_location', 'change_source_location'):
            self._set_change_source_location()
        elif self.technical_name in ('add_boxes_before_cluster', 'multiple_boxes_for_one_transfer'):
            return self._set_add_boxes_before_cluster()
        elif self.technical_name in ('manage_packages', 'confirm_source_package', 'scan_destination_package'):
            return self.set_related_package_fields(self._get_group_settings('group_stock_tracking_lot'))
        elif self.technical_name in ('manage_product_owner'):
            self.set_manage_product_owner_fields(self._get_group_settings('group_stock_tracking_owner'))
        elif self.technical_name in ('apply_default_lots'):
            self.set_apply_default_lots_fields(self._get_group_settings('group_stock_production_lot'))

    def _get_group_settings(self, key):
        return self.env['res.config.settings'].default_get(
            [
                'group_stock_tracking_lot',
                'group_stock_tracking_owner',
                'group_stock_production_lot',
            ]
        ).get(key)

    def _get_warning(self, message):
        return {'warning': {
                'title': 'Another Settings were changed automatically!',
                'message': message,
            }}

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

    def set_apply_default_lots_fields(self, group_stock_production_lot):
        if self.env.context.get('disable_apply_default_lots'):
            self.value = self.env.ref('ventor_base.bool_false')
        elif not group_stock_production_lot and self.value == self.env.ref('ventor_base.bool_true'):
            self.value = self.env.ref('ventor_base.bool_false')

    def _set_add_boxes_before_cluster(self):
        if self.technical_name == 'add_boxes_before_cluster' and self.value == self.env.ref('ventor_base.bool_true'):
            multiple_boxes_for_one_transfer = self.env['ventor.option.setting'].search(
                [
                    ('action_type', '=', self.action_type),
                    ('technical_name', '=', 'multiple_boxes_for_one_transfer'),
                ]
            )
            if multiple_boxes_for_one_transfer.value == self.env.ref('ventor_base.bool_true'):
                multiple_boxes_for_one_transfer.value = self.env.ref('ventor_base.bool_false')
                return self._get_warning(
                    'Because you changed "Add boxes before cluster" to True, '
                    'automatically the following settings were also changed: '
                    '\n- "Multiple boxes for one transfer" was changed to False'
                )
        elif self.technical_name == 'multiple_boxes_for_one_transfer' and self.value == self.env.ref('ventor_base.bool_true'):
            add_boxes_before_cluster = self.env['ventor.option.setting'].search(
                [
                    ('action_type', '=', self.action_type),
                    ('technical_name', '=', 'add_boxes_before_cluster'),
                ]
            )
            if add_boxes_before_cluster.value == self.env.ref('ventor_base.bool_true'):
                self.value = self.env.ref('ventor_base.bool_false')
    
    def _set_change_source_location(self):
        if self.technical_name == 'confirm_source_location' and self.value == self.env.ref('ventor_base.bool_false'):
            change_source_location = self.env['ventor.option.setting'].search(
                [
                    ('action_type', '=', self.action_type),
                    ('technical_name', '=', 'change_source_location'),
                ]
            )
            change_source_location.value = self.env.ref('ventor_base.bool_false')
            return self._get_warning(
                'Because you changed "​Confirm source location" to False, '
                'automatically the following settings were also changed: '
                '\n- "Change source location" was changed to False'
            )
        elif self.technical_name == 'change_source_location' and self.value == self.env.ref('ventor_base.bool_true'):
            confirm_source_location = self.env['ventor.option.setting'].search(
                [
                    ('action_type', '=', self.action_type),
                    ('technical_name', '=', 'confirm_source_location'),
                ]
            )
            if confirm_source_location.value == self.env.ref('ventor_base.bool_false'):
                self.value = self.env.ref('ventor_base.bool_false')

    def set_manage_product_owner_fields(self, group_stock_tracking_owner):
        if self.env.context.get('disable_manage_product_owner'):
            self.value = self.env.ref('ventor_base.bool_false')
        elif not group_stock_tracking_owner and self.value == self.env.ref('ventor_base.bool_true'):
            self.value = self.env.ref('ventor_base.bool_false')
    
    def set_related_package_fields(self, group_stock_tracking_lot):
        if self.env.context.get('enable_putaway_manage_packages'):
            self.value = self.env.ref('ventor_base.bool_true')
        elif self.env.context.get('disable_package_fields'):
            self.value = self.env.ref('ventor_base.bool_false')
        elif not group_stock_tracking_lot:
            self.value = self.env.ref('ventor_base.bool_false')
        elif group_stock_tracking_lot:
            manage_packages = self.env['ventor.option.setting'].search(
                [
                    ('action_type', '=', self.action_type),
                    ('technical_name', '=', 'manage_packages'),
                ]
            )
            if self.value.setting_value == 'False' and self.technical_name == 'manage_packages':
                relate_manage_packages_fields = self.env['ventor.option.setting'].search(
                    [
                        ('action_type', '=', self.action_type),
                        ('technical_name', 'in', ('confirm_source_package', 'scan_destination_package')),
                    ]
                )
                relate_manage_packages_fields.value = self.env.ref('ventor_base.bool_false')
                return self._get_warning(
                    'Because you changed "Show packages fields" to False, '
                    'automatically the following settings were also changed: '
                    '\n- "Confirm source package" was changed to False'
                    '\n- "Force destination package scan" was changed to False'
                )
            if manage_packages.value.setting_value == 'False' and self.technical_name != 'manage_packages':
                self.value = self.env.ref('ventor_base.bool_false')
    
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
