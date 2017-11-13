# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _


class StockRequest(models.Model):
    _inherit = "stock.request"

    purchase_ids = fields.One2many('purchase.order',
                                   compute='_compute_purchase_ids',
                                   string='Pickings', readonly=True)
    purchase_count = fields.Integer(string='Purchase count',
                                    compute='_compute_purchase_ids',
                                    readonly=True)
    purchase_line_ids = fields.Many2many('purchase.order.line',
                                         string='Purchase Order Lines',
                                         readonly=True)

    @api.depends('purchase_ids')
    def _compute_purchase_ids(self):
        for request in self:
            request.purchase_ids = request.purchase_line_ids.mapped('order_id')
            request.purchase_count = len(request.purchase_ids)

    @api.multi
    def action_view_purchase(self):
        action = self.env.ref(
            'purchase.purchase_order_action_generic').read()[0]

        purchases = self.mapped('purchase_ids')
        if len(purchases) > 1:
            action['domain'] = [('id', 'in', purchases.ids)]
        elif purchases:
            action['views'] = [
                (self.env.ref('purchase.purchase_order_form').id, 'form')]
            action['res_id'] = purchases.id
        return action

    @api.depends('purchase_line_ids', 'purchase_line_ids.state')
    def _compute_qty(self):
        res = super(StockRequest, self)._compute_qty()
        for request in self:
            rounding_method = self._context.get('rounding_method', 'UP')
            done_qty = sum(request.purchase_line_ids.move_ids.filtered(
                lambda s: s.state == 'done').mapped('product_qty'))
            qty_in_progress = sum(request.purchase_line_ids.move_ids.filtered(
                lambda s: s.state not in ['done', 'cancel']).mapped(
                'product_qty'))
            request.qty_done += request.product_id.uom_id._compute_quantity(
                done_qty, request.product_uom,
                rounding_method=rounding_method)
            request.qty_in_progress += \
                request.product_id.uom_id._compute_quantity(
                    qty_in_progress, request.product_uom,
                    rounding_method=rounding_method)
        return res
