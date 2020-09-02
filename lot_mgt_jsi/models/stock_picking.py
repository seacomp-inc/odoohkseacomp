# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    show_existing_lot_button = fields.Boolean(string="Show Button for add Existing Lot")


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    lot_name = fields.Char("Lot Name")
    existing_lot_id = fields.Many2one('stock.production.lot', 'Existing Lot')
 
    def button_add_lot(self):
        if self.lot_name:
            self.write({'move_line_nosuggest_ids': [(0, 0, {
                                                            'picking_id':self.id, \
                                                            'product_id': line.product_id.id, \
                                                            'qty_done': line.product_uom_qty, \
                                                            'product_uom_id': line.product_uom.id, \
                                                            'location_id': line.location_id.id, \
                                                            'location_dest_id': line.location_dest_id.id, \
                                                            'lot_name': self.lot_name}) for line in self.move_ids_without_package]})

    def button_add_existing_lot(self):
        if self.existing_lot_id:
            new_lines = []
            lot = self.env['stock.production.lot']
            for line in self.move_line_ids:
                lot = lot.search([('product_id', '=', line.product_id.id), ('name', '=', self.existing_lot_id.name)])
                if lot:
                    line.lot_id = lot.id
