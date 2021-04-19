# -*- coding: utf-8 -*-

import datetime

from odoo import api, fields, models


class Partner(models.Model):
    _inherit = "res.partner"

    remaining_credit = fields.Monetary(string='Remaining Credit', compute="_compute_remaining_credit", store=False)

    @api.depends('credit', 'credit_limit')
    def _compute_remaining_credit(self):
        for partner in self:
            partner.remaining_credit = partner.credit_limit - partner.credit
