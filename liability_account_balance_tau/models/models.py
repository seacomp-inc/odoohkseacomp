# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    x_liability_account_balance = fields.Float(compute='_calculate_liability_account_balance', string="Liability Amount Balance", store=True)
    x_cash_availability =  fields.Float(compute='_calculate_cash_availability', string='Cash Availability', store=True)


    @api.depends('x_stuido_max_loan_amount', 'x_liability_account_balance')
    def _calculate_cash_availability(self):
        for account in self:
            account.x_cash_availability = account.x_stuido_max_loan_amount - account.x_liability_account_balance


    @api.depends('x_studio_related_liability_account')
    def _calculate_liability_account_balance(self):
        for account in self:
            account.x_liability_account_balance = sum(self.env['account.move.line'].search([['account_id','=',account.x_studio_related_liability_account.id]]).mapped('balance'))
