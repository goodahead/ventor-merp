# Copyright 2022 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

# Odoo:
from odoo import fields, models
from odoo.fields import Datetime


class ProductionLot(models.Model):
    _inherit = "stock.production.lot"

    name = fields.Char(
        "Lot/Serial Number",
        default=lambda self: self._get_lot_name(),
    )

    def _get_lot_name(self):
        picking_id = self.env.context.get("active_picking_id")
        if picking_id:
            lot_sequence_id = (
                self.env["stock.picking"]
                .browse(picking_id)
                .picking_type_id.warehouse_id.lot_sequence_id
            )
            if lot_sequence_id:
                return lot_sequence_id.with_context(use_daily_sequence=True).next_by_code(
                    lot_sequence_id.code, sequence_date=Datetime.now()
                )
        return self.env["ir.sequence"].next_by_code("stock.lot.serial")
