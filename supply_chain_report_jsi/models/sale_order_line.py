# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.tools import safe_eval

class saleOrderLine(models.Model):
    _inherit = "sale.order.line"

    cost_total = fields.Float('Total Cost', compute="_compute_costing", store="True")
    profit_loss = fields.Float('Profit / Loss', compute="_compute_costing", store="True")
    margin_new = fields.Float('Margin', compute="_compute_costing", store="True")

    @api.depends('product_uom_qty', 'purchase_price')
    def _compute_costing(self):
        for line in self:
            if line.product_uom_qty:
                # cost_total
                line.cost_total = line.product_uom_qty * line.purchase_price
                # profit_loss
                line.profit_loss = line.price_subtotal - line.cost_total
                # margin_new
                line.margin_new = line.profit_loss / line.price_subtotal

    @api.multi
    def open_supply_chain_report(self):
        [action] = self.env.ref('supply_chain_report_jsi.action_stock_move_supply_chain_report_jsi').read()
        action['context'] = dict(safe_eval(action.get('context')), active_id=self.product_id.id, search_default_product_id=self.product_id.id)
        return action
