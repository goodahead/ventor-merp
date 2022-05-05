# Copyright 2022 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

# Odoo:
from odoo import _, api, models


class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    @api.onchange("lot_name", "lot_id")
    def _onchange_serial_number(self):
        res = super()._onchange_serial_number()
        if self.product_id.tracking == "lot" and not self.lot_name:
            lot_name = self.lot_id.with_context(
                active_picking_id=self.move_id.picking_id.id
            )._get_lot_name()
            self.lot_name = lot_name
        return res
