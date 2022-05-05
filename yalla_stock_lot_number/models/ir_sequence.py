# Copyright 2022 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

# Odoo:
from odoo import _, fields, models


class IrSequence(models.Model):
    _inherit = "ir.sequence"

    def _create_date_range_seq(self, date):
        res = super()._create_date_range_seq(date)
        if self.env.context.get("use_daily_sequence"):
            res.date_from = res.date_to = fields.Datetime.now().date()
        return res
