# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import _, api, models
from odoo.exceptions import UserError


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    @api.constrains("result_package_id")
    def _validate_destination_package(self):
        for sml in self:
            sml_same_package_ids = self.search(
                [
                    ("state", "not in", ("done", "cancel")), 
                    ("result_package_id", "=", sml.result_package_id.id), 
                    ("location_dest_id", "!=", sml.location_dest_id.id),
                ]
            )
            if sml_same_package_ids:
                raise UserError(
                    _(  
                        'You cannot move the same package content more than once '
                        'in the same transfer or split the same package into two location.\n'
                        'This package is used in source document %s', ', '.join(set(sml_same_package_ids.mapped("origin")))
                    )
                )
 