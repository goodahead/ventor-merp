# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import models, fields


class Company(models.Model):
    _inherit = 'res.company'

    outgoing_routing_strategy = fields.Selection(
        [
            ('location_id.removal_prio', 'Location removal priority'),
            ('location_id.name', 'Location name'),
        ],
        string='Picking Strategy', default='location_id.name')

    outgoing_routing_order = fields.Selection(
        [
            ('0', 'Ascending (A-Z)'),
            ('1', 'Descending (Z-A)'),
        ],
        string='Picking Order', default='0')
