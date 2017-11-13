# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    stock_request_id = fields.Many2one('stock.request', 'Stock Request')
