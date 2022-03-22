# Odoo:
from odoo import SUPERUSER_ID, _, api


def migrate(cr, version):

    env = api.Environment(cr, SUPERUSER_ID, {})
    company_ids = env['res.company'].with_context(active_test=False).search([])
    for company in company_ids:
        if company.outgoing_routing_strategy == 'name':
            company.outgoing_routing_strategy = 'location_id.name'
        else:
            company.outgoing_routing_strategy = 'location_id.removal_prio'
