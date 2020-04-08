# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    customer_info_ids = fields.One2many('product.customer_info', 'product_tmpl_id', 'Customer')