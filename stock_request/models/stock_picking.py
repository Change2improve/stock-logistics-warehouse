# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    stock_request_id = fields.Many2one(related="group_id.stock_request_id",
                                       string="Stock Request", store=True)
