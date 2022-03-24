# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import models, tools


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    def _compute_mimetype(self, values):
        if values.get('name') == 'logotype_file':
            tools.base64_to_image(values.get('datas'))
        res = super()._compute_mimetype(values)
        return res
