# Odoo:
from odoo import api, SUPERUSER_ID


def migrate(cr, version):

    env = api.Environment(cr, SUPERUSER_ID, {})
    company_ids = env['res.company'].with_context(active_test=False).search([])
    logotype_file = env['ventor.setting'].get_param('logo.file')
    if logotype_file:
        company_ids.logotype_file = logotype_file
