# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductApproval(models.Model):
    _inherit = 'product.template'
    
    product_state = fields.Selection([
        ('draft', 'In Development'),
        ('sellable', 'Normal'),
        ('end', 'End of Lifecycle'), 
        ('obsolete', 'Obsolete')], string="Product Status", default='draft', store='True', track_visibility='onchange')
    
    engineering_approved = fields.Boolean(string="Engineering", store='True', track_visibility='onchange')
    product_approved = fields.Boolean(string="Production", store='True', track_visibility='onchange')
    quality_approved = fields.Boolean(string="Quality", store='True', track_visibility='onchange')
    product_state_read_only = fields.Selection([
        ('draft', 'In Development'),
        ('sellable', 'Normal'),
        ('end', 'End of Lifecycle'), 
        ('obsolete', 'Obsolete')],string="Product Status Read-Only", default='draft', store='True')
    engineering_approved_read_only = fields.Boolean(string="Engineering Read-Only", store='True')
    product_approved_read_only = fields.Boolean(string="Production Read-Only", store='True')
    quality_approved_read_only = fields.Boolean(string="Quality Read-Only", store='True')
    chinese_name = fields.Char(string="Chinese Product Name", store='True', index='True')
    