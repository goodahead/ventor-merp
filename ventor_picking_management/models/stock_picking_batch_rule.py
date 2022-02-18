# Copyright 2021 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).


# Odoo:
from odoo import api, fields, models


class StockPickingBatchRule(models.Model):
    _name = "stock.picking.batch.rule"

    name = fields.Char(required=True)
    rule_action = fields.Selection([('add_to_draft_batch', 'Add to  Draft Transfer for current WH')], required=True, string='Do')
    rule_criteria = fields.Char(string='If') # обавить виджет domain
    rule_trigger = fields.Selection([('sales_order_confirmed', 'Sales Order Confirmed')], required=True, string='When')
