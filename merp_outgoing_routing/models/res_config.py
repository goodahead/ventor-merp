# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class StockConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    outgoing_routing_strategy = fields.Selection(
        [
            ('location_id.removal_prio', 'Location removal priority'),
            ('location_id.name', 'Location name'),
        ],
        string='Picking Strategy',
        related='company_id.outgoing_routing_strategy',
        readonly=False)

    outgoing_routing_order = fields.Selection(
        [
            ('0', 'Ascending (A-Z)'),
            ('1', 'Descending (Z-A)'),
        ],
        string='Picking Order',
        related='company_id.outgoing_routing_order',
        readonly=False)
