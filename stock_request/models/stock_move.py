# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'

    stock_request_id = fields.Many2one('stock.request', 'Stock Request')
