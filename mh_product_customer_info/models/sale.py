from odoo import models, fields, api

class SaleOrderLine(models.Model):

    _inherit = 'sale.order.line'

    cust_code = fields.Char('Customer P/N', store = True, default = "N/A")
    
    @api.onchange('product_id')
    def product_id_change(self):
        super(SaleOrderLine, self).product_id_change()
        if self.product_id and self.order_partner_id:
            self.cust_code = self.product_id.product_tmpl_id.customer_info_ids.filtered(lambda x: x.name == self.order_partner_id).product_ref 
