# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class CustomerProductInfo(models.Model):
    _name = 'product.customer_info'
    _rec_name = 'product_ref'

    name = fields.Many2one('res.partner', 'Customer')
    product_tmpl_id = fields.Many2one('product.template', 'MH Product')
    product_name = fields.Char('Customer Product Name')
    product_ref = fields.Char('Customer Product Code')
    product_url = fields.Char('Customer Product URL')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1)

    @api.constrains('name')
    def _check_customer(self):
        if self.search_count([
            ('name', '=', self.name.id),
           ('product_tmpl_id', '=', self.product_tmpl_id.id),
        ]) > 1:
            raise ValidationError(_("This product of %s has been registered with a Customer Product Code before. Please choose a different customer or product.") % self.name.name)
