from datetime import datetime, timedelta
# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo import models, fields, api
# import logging
# logger =logging.getLogger(__name__)



class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    mh_reference = fields.Char(string="MH Reference No.", related="order_id.mh_reference")
    product_code = fields.Char(string="MH Product Code", related="product_id.default_code")
    
#    requested_date = fields.Datetime('Requested Date', related='order_id.requested_date', store='true', track_visibility='onchange')#
    
    requested_date = fields.Datetime(string="Requested Date", store='True', track_visibility='onchange')
    confirmed_delivery_date = fields.Datetime(string="Confirmed Delivery Date", store='True', track_visibility='onchange')
    
    
#    @api.onchange('requested_date')
#    def _onchange_requested_date(self):
#        self.confirmed_delivery_date = self.requested_date