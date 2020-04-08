# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, api
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
# from odoo import models, fields, api, _
# import odoo.addons.decimal_precision as dp
# from odoo.exceptions import UserError
# from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
# import logging
# logger =logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"
    
    customer_po_num = fields.Char(string = "Customer PO No.")
    mh_reference = fields.Char(string="MH Reference No.")
    requested_date = fields.Datetime('SO Requested Date', store='True', track_visibility='onchange')
    confirmed_delivery_date = fields.Datetime(string="SO Confirmed Delivery Date", store='True', track_visibility='onchange')
    
#    state = fields.Selection([
#        ('draft', 'Draft'),
#        ('sale', 'Confirmed'),
#        ('done', 'Done'),
#        ('cancel', 'Cancelled')])
#    revision = fields.Char(string="Revision No.")
#    client_order_ref = fields.Char(string='Customer Reference No.')

    
#    def action_confirm(self):
#        super(SaleOrder, self).action_confirm()
#        if self.order_line:
#            self.requested_date = max(self.order_line.mapped('requested_date'))
            
#    @api.onchange('date_order')
#    def _change_line_requested_date(self):
#        if self.order_line:
#            for order_line_id in self.order_line:
#                order_line_id._set_requested_date()

