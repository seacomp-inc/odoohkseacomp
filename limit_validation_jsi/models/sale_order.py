# -*- coding: utf-8 -*-

import datetime

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class saleOrder(models.Model):
    _inherit = "sale.order"

    is_overdue_limit_end = fields.Boolean('Is Overdue?', compute="_compute_remaining_qty")
    remaining_credit = fields.Monetary(string='Remaining Credit', compute="_compute_remaining_credit")

    @api.depends('partner_id.credit', 'partner_id.credit_limit')
    def _compute_remaining_credit(self):
        for order in self:
            order.remaining_credit = order.partner_id.credit_limit - order.partner_id.credit

    @api.depends('partner_id.commercial_partner_id.unreconciled_aml_ids', 'company_id.allowed_overdue_limit_days')
    def _compute_remaining_qty(self):
        for order in self:
            if order.partner_id and order.company_id.allowed_overdue_limit_days:
                today = fields.Date.today()
                limit_days = order.company_id.allowed_overdue_limit_days
                date_list = order.partner_id.commercial_partner_id.unreconciled_aml_ids.mapped('date_maturity')
                for date in date_list:
                    if (today - date).days > limit_days:
                        order.is_overdue_limit_end = True
                        break

    def action_confirm(self):
        if self.env.user.has_group('account.group_account_manager'):
            return super().action_confirm()
        if self.remaining_credit <= 0:
            raise UserError(_("This customer is over credit limit. To proceed, please contact Mike."))
        if self.is_overdue_limit_end:
            raise UserError(_("The AR for this customer are overdue. To proceed, please contact Mike."))
        return super().action_confirm()
