# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class StockConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    outgoing_routing_strategy = fields.Selection(
        [
            ('location_id.name', 'Sort by source locations in alphabetical order'),
            ('location_id.removal_prio', 'Sort by location removal strategy priority field'),
        ],
        string='Routing Strategy', default='location_id.name',
        related='company_id.outgoing_routing_strategy')

    outgoing_routing_order = fields.Selection(
        [
            (0, 'Ascending (A-Z)'),
            (1, 'Descending (Z-A)'),
        ],
        string='Routing Order', default=0,
        related='company_id.outgoing_routing_order')
