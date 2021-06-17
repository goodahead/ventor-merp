# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockInventory(models.Model):
    _name = 'stock.inventory'
    _inherit = ['stock.inventory', 'stock.location.mixin']

    def _onchange_company_id(self):
        super(StockInventory, self)._onchange_company_id(default)
        # Apply logic only in multi-location environment
        if self.user_has_groups('stock.group_stock_multi_locations'):
            location_id = self._get_default_location_warehouse()
            if location_id:
                self.location_ids = location_id


class InventoryLine(models.Model):
    _inherit = "stock.inventory.line"
    _description = "Inventory Line"

    @api.constrains("prod_lot_id")
    def _check_product_lot(self):
        """ check product lot/serial except for stock_fix_lot """
        if self.env.context.get("skip_product_lot_check") and not self.product_qty:
                return
        lot_validation = self.env['ventor.config'].search([('key', '=', 'ventor_base.force_lot_validation_on_inventory_adjustment')]).mapped('value')
        if lot_validation:
            for product in self:
                if product.product_tracking in ("lot", "serial") and not product.prod_lot_id:
                    raise ValidationError(
                        _(
                            "You need to supply a Lot/Serial number for product: %s",
                            product.product_id.display_name,
                        )
                    )