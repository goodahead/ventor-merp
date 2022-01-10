# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import _, api, models
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.constrains("result_package_id")
    def _validate_destination_package(self):
        for sml in self:
            if sml.result_package_id:
                sml_same_package_ids = self.search(
                    [
                        ("state", "not in", ("done", "cancel")),
                        ("result_package_id", "=", sml.result_package_id.id),
                        ("location_dest_id", "!=", sml.location_dest_id.id),
                    ]
                )
                if sml_same_package_ids:
                    documents = ', '.join(set(sml.origin for sml in sml_same_package_ids if sml.origin))
                    add_message = _(' This package %s is used in following documents %s', sml.result_package_id.display_name, documents) if documents else ''
                    raise UserError(
                        _(
                            'You cannot split the same package in two locations.' + add_message
                        )
                    )
