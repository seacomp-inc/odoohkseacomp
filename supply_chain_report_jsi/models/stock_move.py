# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    check_transfer_date = fields.Boolean(string="Ignore Transfer Date")


class StockMove(models.Model):
    _inherit = "stock.move"

    commitment_date = fields.Date('Commitment date', compute="_compute_commitment_date", store="True")
    calc_on_hand_qty = fields.Float('Warehouse QOH')
    calc_forecasted_qty = fields.Float('Warehouse Forecasted')
    run_total = fields.Float('Run Total')
    comment = fields.Text('Comments')
    date_internal_transfer = fields.Date('Internal Transfer Date')

    @api.constrains('date_internal_transfer')
    def check_internal_transfer_date(self):
        # TODO: need to refactor, can we simply go with picking type?
        for move in self:
            if not(move.workorder_id \
                   or move.production_id \
                   or move.purchase_line_id \
                   or move.sale_line_id \
                   or move.picking_type_id.check_transfer_date \
                   or move.date_internal_transfer):
                raise ValidationError(_("Internal Transfer Date is required!"))

    @api.depends('date_internal_transfer', 'sale_line_id.x_studio_confirmed_delivery_date', 'purchase_line_id.date_planned', 'picking_id.backorder_id')
    def _compute_commitment_date(self):
        for move in self:
            if move.sale_line_id:
                move.commitment_date = fields.Date.to_string(move.sale_line_id.x_studio_confirmed_delivery_date)
            elif move.purchase_line_id:
                move.commitment_date = fields.Date.to_string(move.purchase_line_id.date_planned)
            else:
                move.commitment_date = move.date_internal_transfer and fields.Date.to_string(move.date_internal_transfer) or False

    def _compute_qty(self):
        for move in self:
            warehouse = move.warehouse_id

            # calc_on_hand_qty
            move.calc_on_hand_qty = move.product_id.with_context(warehouse=warehouse.id).qty_available

            moves_in_out = move.search([
                ('warehouse_id', '=', warehouse.id),
                ('product_id', '=', move.product_id.id),
                ('picking_code', 'in', ['incoming', 'outgoing']),
                ('state', 'not in', ['draft', 'done', 'cancel']),
                ('commitment_date', '!=', False),
                # ('id', '!=', move.id),
                ])

            # calc_forecasted_qty
            moves_in = moves_in_out.filtered(lambda x: x.picking_code == 'incoming')
            moves_out = moves_in_out.filtered(lambda x: x.picking_code == 'outgoing')
            move.calc_forecasted_qty = move.calc_on_hand_qty + sum(moves_in.mapped('product_uom_qty')) - sum(moves_out.mapped('product_uom_qty'))

            # run_total
            move_in_qty = sum(moves_in.filtered(lambda x: x.commitment_date.strftime('%Y-%m-%d') <= move.commitment_date.strftime('%Y-%m-%d')).mapped('product_uom_qty'))
            move_out_qty = sum(moves_out.filtered(lambda x: x.commitment_date.strftime('%Y-%m-%d') <= move.commitment_date.strftime('%Y-%m-%d')).mapped('product_uom_qty'))
            move.run_total = move.calc_on_hand_qty - move_out_qty + move_in_qty

class StockPicking(models.Model):
    _inherit = "stock.picking"

    date_internal_transfer_new = fields.Date('New Transfer Date')

    @api.multi
    def action_update_transfer_date(self):
        self.ensure_one()
        if self.date_internal_transfer_new:
            self.move_ids_without_package.write({'date_internal_transfer': self.date_internal_transfer_new})
