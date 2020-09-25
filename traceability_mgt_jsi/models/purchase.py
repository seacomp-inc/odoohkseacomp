# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    mh_tracking_no = fields.Char(string='MH Tracking No.', copy=True)

    @api.model
    def _prepare_picking(self):
        res = super(PurchaseOrder, self)._prepare_picking()
        self.group_id['mh_tracking_no'] = self.mh_tracking_no
        res['mh_tracking_no'] = self.mh_tracking_no
        return res

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    mh_tracking_no = fields.Char(related='order_id.mh_tracking_no', store=True, string='MH Tracking No.', readonly=True)