# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_overdue_limit_end = fields.Boolean('Is Overdue?', compute="_compute_remaining_qty")
    currency_id = fields.Many2one(related='partner_id.currency_id')
    remaining_credit = fields.Float(string='Remaining Credit', compute="_compute_remaining_credit", store=False)

    @api.depends('partner_id.credit', 'partner_id.credit_limit')
    def _compute_remaining_credit(self):
        for picking in self:
            picking.remaining_credit = picking.partner_id.credit_limit - picking.partner_id.credit

    @api.depends('partner_id.commercial_partner_id.unreconciled_aml_ids', 'company_id.allowed_overdue_limit_days')
    def _compute_remaining_qty(self):
        for picking in self:
            if picking.partner_id and picking.company_id.allowed_overdue_limit_days:
                today = fields.Date.today()
                limit_days = picking.company_id.allowed_overdue_limit_days
                date_list = picking.partner_id.commercial_partner_id.unreconciled_aml_ids.mapped('date_maturity')
                for date in date_list:
                    if (today - date).days > limit_days:
                        picking.is_overdue_limit_end = True
                        break

    def button_validate(self):
        if self.env.user.has_group('account.group_account_manager'):
            return super().button_validate()
        if self.picking_type_code == 'outgoing' and self.remaining_credit <= 0:
            raise UserError(_("This customer is over credit limit. To proceed, please contact Mike."))
        if self.is_overdue_limit_end:
            raise UserError(_("The AR for this customer are overdue. To proceed, please contact Mike."))
        return super().button_validate()
