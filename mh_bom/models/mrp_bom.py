# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, api
import odoo.addons.decimal_precision as dp

# from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
# from odoo import models, fields, api, _
# from odoo.exceptions import UserError
# from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
# import logging
# logger =logging.getLogger(__name__)


class MhMrpBomLiner(models.Model):
    _inherit = "mrp.bom"
    
    code = fields.Selection([
        ('Finished Goods','Finished Goods'),
        ('Sub Assembly','Sub Assembly')], store="True", string="BOM Reference")

    
    @api.model
    def get_currency(self):
        return self.env.user.company_id.currency_id
        
#    @api.multi
#    @api.depends('bom_line_ids', 'bom_line_ids.product_id','bom_line_ids.product_id.standard_price')
#    def _compute_bom_cost_total(self):
#        for rec in self:
#            rec.total_cost = 0.0
#            for line in rec.bom_line_ids:
#                rec.total_cost += line.product_id.standard_price * line.product_qty
    
#    total_cost = fields.Float(
#        string='Total Cost', 
#        store=True,
#        compute='_compute_bom_cost_total', 
#        digits=dp.get_precision('Product Price'),
#    )
    
    currency_id = fields.Many2one(
        'res.currency', string='Currency', 
        default=get_currency,
    )