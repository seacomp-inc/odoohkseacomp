# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from odoo import models, fields, api


class MhMrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    designator = fields.Char(string="Designator", stored=True)
    description = fields.Char(string="Component Description", stored=True)
    product_code = fields.Char(string='MH Part Number', related='product_id.default_code')
#    mfgr_code = fields.ManytoOne('mfgr_code','product_id', string='Mfgr P/N', stored=True, domain={[]})