# -*- coding: utf-8 -*-

import itertools

from odoo.addons import decimal_precision as dp

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, RedirectWarning, UserError
from odoo.osv import expression
from odoo.tools import pycompat


class mhPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'
    
    mh_reference = fields.Char(string="MH Reference No.", related="order_id.mh_reference")
    vendor_ship_date = fields.Datetime('Vendor Shipment Date', store='True', track_visibility='onchange')
    confirmed_vendor_ship_date = fields.Datetime(string="Confirmed Shipment Date", store='True', track_visibility='onchange')
    
    origin = fields.Char(string="Source Document", related="order_id.origin")
    product_code = fields.Char(string="Code", related="product_id.default_code")
    qty_unbilled = fields.Float(compute='_compute_qty_unbilled', string="Unbilled Qty", digits=dp.get_precision('Product Unit of Measure'), store=True)

    
#    standard_price = fields.Float(
#        'Unit Cost', compute='_compute_standard_price', search='_search_standard_price', digits=dp.get_precision('Product #Price'), help = "This Cost is for reference at this instance.")



#    @api.depends('product_id','state')
#    def _compute_standard_price(self):
#        if self.state in ['draft','sent','to approve']:
#            unique_variants = self.filtered(lambda template: len(template.product_id.product_variant_ids) == 1)
#            for template in unique_variants:
#                template.standard_price = template.product_id.product_variant_ids.standard_price


#   def _search_standard_price(self, operator, value):
#        products = self.env['product.product'].search([('standard_price', operator, value)], limit=None)
#        return [('id', 'in', products.mapped('product_tmpl_id').ids)]
    
    
# When the purchase order is confirmed, hide Cost column in
# purchase.order.form 
#  <field name="standard_price" attrs="{'column_invisible': [('parent.state', 'in', ('purchase', 'done'))]}"/>
# 

    
    @api.depends('qty_received', 'qty_invoiced')
    def _compute_qty_unbilled(self):
        for line in self:
            line.qty_unbilled = line.qty_received - line.qty_invoiced


    @api.onchange('product_id')
    def onchange_product_id(self):
        res = super(mhPurchaseOrderLine, self).onchange_product_id()
        self.confirmed_vendor_ship_date = self.date_planned
#        if not self.taxes_id:
#            fpos = self.order_id.fiscal_position_id
#            taxes = self.product_id.categ_id.property_account_expense_categ_id.tax_ids
#            if taxes:
#                self.taxes_id = fpos.map_tax(taxes) if fpos else taxes
        return res