# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class StockMove(models.Model):
    _inherit = "stock.move"

    commitment_date = fields.Date('Commitment date', compute="_compute_commitment_date", store="True")
    calc_on_hand_qty = fields.Float('Warehouse QOH', compute="_compute_qty", store="True")
    calc_forecasted_qty = fields.Float('Warehouse Forecasted', compute="_compute_qty", store="True")
    run_total = fields.Float('Run Total', compute="_compute_qty", store="True")
    comment = fields.Text('Comments')
    date_internal_transfer = fields.Date('Commitment date')

    @api.depends('date_internal_transfer', 'sale_line_id.x_studio_confirmed_delivery_date', 'purchase_line_id.date_planned')
    def _compute_commitment_date(self):
        for move in self:
            if move.sale_line_id:
                move.commitment_date = fields.Date.to_string(move.sale_line_id.x_studio_confirmed_delivery_date)
            elif move.purchase_line_id:
                move.commitment_date = fields.Date.to_string(move.purchase_line_id.date_planned)
            else:
                move.commitment_date = fields.Date.to_string(move.date_internal_transfer)

    @api.depends('commitment_date', 'warehouse_id', 'picking_type_id.warehouse_id', 'product_id.qty_available')
    def _compute_qty(self):
        for move in self:
            warehouse = move.warehouse_id
            if warehouse and move.state not in ['draft', 'done', 'cancel']:
                # calc_on_hand_qty
                move.calc_on_hand_qty = move.product_id.with_context(warehouse=warehouse.id).qty_available

                moves_in_out = move.search([
                    ('warehouse_id', '=', warehouse.id),
                    ('product_id', '=', move.product_id.id),
                    ('picking_code', 'in', ['incoming', 'outgoing']),
                    ('state', 'not in', ['draft', 'done', 'cancel']),
#                     ('id', '!=', move.id),
                    ])

                # calc_forecasted_qty
                moves_in = moves_in_out.filtered(lambda x: x.picking_code == 'incoming')
                moves_out = moves_in_out.filtered(lambda x: x.picking_code == 'outgoing')
                move.calc_forecasted_qty = move.calc_on_hand_qty + sum(moves_in.mapped('product_uom_qty')) - sum(moves_out.mapped('product_uom_qty'))

                # run_total
                move_in_qty = sum(moves_in.filtered(lambda x: x.commitment_date.strftime('%Y-%m-%d') <= move.commitment_date.strftime('%Y-%m-%d')).mapped('product_uom_qty'))
                move_out_qty = sum(moves_out.filtered(lambda x: x.commitment_date.strftime('%Y-%m-%d') <= move.commitment_date.strftime('%Y-%m-%d')).mapped('product_uom_qty'))
                move.run_total = move.calc_on_hand_qty - move_out_qty + move_in_qty
