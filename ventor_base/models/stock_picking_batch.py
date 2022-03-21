# Copyright 2022 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

# Odoo:
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockPickingBatch(models.Model):
    _inherit = "stock.picking.batch"

    allowed_picking_ids = fields.One2many("stock.picking", compute="_compute_allowed_picking_ids")

    picking_ids = fields.One2many(
        "stock.picking",
        "batch_id",
        string="Transfers",
        readonly=True,
        domain="[('id', 'in', allowed_picking_ids)]",
        check_company=True,
        states={"draft": [("readonly", False)], "in_progress": [("readonly", False)]},
        help="List of transfers associated to this batch",
    )

    picking_type_id = fields.Many2one(
        "stock.picking.type",
        "Operation Type",
        check_company=True,
        copy=False,
        readonly=True,
        states={"draft": [("readonly", False)]},
    )

    @api.depends("company_id", "picking_type_id", "state")
    def _compute_allowed_picking_ids(self):
        allowed_picking_states = ["waiting", "confirmed", "assigned"]
        cancelled_batchs = self.env["stock.picking.batch"].search_read(
            [("state", "=", "cancel")], ["id"]
        )
        cancelled_batch_ids = [batch["id"] for batch in cancelled_batchs]

        for batch in self:
            domain_states = list(allowed_picking_states)
            # Allows to add draft pickings only if batch is in draft as well.
            if batch.state == "draft":
                domain_states.append("draft")
            domain = [
                ("company_id", "=", batch.company_id.id),
                ("immediate_transfer", "=", False),
                ("state", "in", domain_states),
                "|",
                "|",
                ("batch_id", "=", False),
                ("batch_id", "=", batch.id),
                ("batch_id", "in", cancelled_batch_ids),
            ]
            if batch.picking_type_id:
                domain += [("picking_type_id", "=", batch.picking_type_id.id)]
            batch.allowed_picking_ids = self.env["stock.picking"].search(domain)

    def write(self, vals):
        res = super().write(vals)
        if vals.get("picking_type_id"):
            self._sanity_check()
        if vals.get("picking_ids"):
            batch_without_picking_type = self.filtered(lambda batch: not batch.picking_type_id)
            if batch_without_picking_type:
                picking = self.picking_ids and self.picking_ids[0]
                batch_without_picking_type.picking_type_id = picking.picking_type_id.id
        return res

    def _sanity_check(self):
        for batch in self:
            if not batch.picking_ids <= batch.allowed_picking_ids:
                erroneous_pickings = batch.picking_ids - batch.allowed_picking_ids
                raise UserError(
                    _(
                        "The following transfers cannot be added to batch transfer %s. "
                        "Please check their states and operation types, if they aren't immediate "
                        "transfers or if they're not already part of another batch transfer.\n\n"
                        "Incompatibilities: %s"
                    )
                    % (batch.name, ", ".join(erroneous_pickings.mapped("name")))
                )
