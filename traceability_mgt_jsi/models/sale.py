# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class saleOrder(models.Model):
    _inherit = "sale.order"

    mh_tracking_no = fields.Char(string='MH Tracking No.', copy=True)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    mh_tracking_no = fields.Char(related='order_id.mh_tracking_no', store=True, string='MH Tracking No.', readonly=True)
