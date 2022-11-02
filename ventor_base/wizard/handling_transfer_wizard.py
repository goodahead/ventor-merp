# Copyright 2022 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

# Odoo:
from odoo import _, fields, models


class HandlingTransferWizard(models.TransientModel):
    _name = "handling.transfer.wizard"
    _description = "Handling Transfer Wizard"

    pallet_id = fields.Many2one("stock.location", string="Pallets")
    destination_location_id = fields.Many2one("stock.location", string="Destination Location")
