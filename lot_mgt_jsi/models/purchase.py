# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    lot_name = fields.Char("Lot Name")

    @api.model
    def _prepare_picking(self):
        res = super(PurchaseOrder, self)._prepare_picking()
        if self.picking_type_id.id == env.ref('__export__.stock_picking_type_21_9ba29550', raise_if_not_found=False):
            res['lot_name'] = self.lot_name
        return res
