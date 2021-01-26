# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools import float_is_zero

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    x_related_liability_account = fields.Many2one('account.account', string='Related Liability Account')
    x_max_loan_amount = fields.Float(string="Max. Loan Amount")
    x_liability_account_balance = fields.Float(compute='_calculate_liability_account_balance', string="Liability Amount Balance")
    x_cash_availability =  fields.Float(compute='_calculate_cash_availability', string='Cash Availability')


    @api.depends('x_max_loan_amount', 'x_liability_account_balance')
    def _calculate_cash_availability(self):
        for account in self:
            account.x_cash_availability = account.x_max_loan_amount - abs(account.x_liability_account_balance)


    @api.depends('x_related_liability_account')
    def _calculate_liability_account_balance(self):
        for account in self:
            balance = sum(self.env['account.move.line'].search([['account_id','=',account.x_related_liability_account.id]]).mapped('balance'))
            #check if balance close to zero -> set to zero
            if float_is_zero(balance, precision_digits=2):
                account.x_liability_account_balance = 0
            else:
                account.x_liability_account_balance = balance
