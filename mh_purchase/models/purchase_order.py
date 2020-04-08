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


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    
    mh_reference = fields.Char(string="MH Reference No.")
    
    @api.multi
    def action_set_date_planned(self):
        for order in self:
            order.order_line.update({'date_planned': order.date_planned})
            
# a method used in purchase.order.form view
#  <button name="action_set_date_planned" type="object" states="draft,sent" string="Set date to all order lines" help="This changes the scheduled date of all order lines to the given date" class="fa fa-calendar o_icon_button oe_edit_only"/>

