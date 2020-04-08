# -*- coding: utf-8 -*-

import itertools

from odoo.addons import decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, RedirectWarning, UserError
from odoo.osv import expression
from odoo.tools import pycompat


class mhProductPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

#standard_price = fields.Float('Unit Cost', compute='_compute_standard_price', search='_search_standard_price', digits=dp.get_precision('Product Price'), help = "This Cost is for reference at this instance.")

    standard_price = fields.Float('Unit Cost', compute='_compute_standard_price', digits=dp.get_precision('Product Price'), help = "This Cost is for reference at this instance.")

    @api.depends('product_id','state')
    def _compute_standard_price(self):
        for line in self:
            if line.state in ['draft','sent','to approve']:
                line.standard_price = line.product_id.standard_price


    def _search_standard_price(self, operator, value):
        products = self.env['product.product'].search([('standard_price', operator, value)], limit=None)
        return [('id', 'in', products.mapped('product_tmpl_id').ids)]

    
#    def _search_standard_price(self, operator, value):
#        products = self.env['product.product'].search([('standard_price', operator, value)], limit=None)
#        return [('id', 'in', products.mapped('product_tmpl_id').ids)]
    
    
# When the purchase order is confirmed, hide Cost column in
# purchase.order.form 
#  <field name="standard_price" attrs="{'column_invisible': [('parent.state', 'in', ('purchase', 'done'))]}"/>
# 
# Please note a product  Standard Price (Cost) will only be updated when the product being received and in "stock", no in "Transit (Delivery Order/Receipt)
