# Copyright 2022 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

# Odoo:
from odoo import _, api, fields, models
from odoo.fields import Datetime


class Warehouse(models.Model):
    _inherit = "stock.warehouse"

    lot_sequence_id = fields.Many2one(
        "ir.sequence",
        string="WH Lot Name Sequence",
        ondelete="cascade",
        readonly=True,
    )

    @api.model
    def create(self, vals):
        res = super(Warehouse, self).create(vals)
        res._create_wh_lot_sequence()
        return res

    def _create_wh_lot_sequence(self):
        self.ensure_one()
        lot_sequence_id = self.env["ir.sequence"].create(
            {
                "name": "{} Sequence".format(self.code),
                "implementation": "standard",
                "code": "stock.warehouse." + self.code.lower(),
                "active": True,
                "company_id": self.company_id.id,
                "prefix": self.code + "%(year)s%(month)s%(day)s-",
                "use_date_range": True,
                "number_increment": 1,
            }
        )
        self.lot_sequence_id = lot_sequence_id
