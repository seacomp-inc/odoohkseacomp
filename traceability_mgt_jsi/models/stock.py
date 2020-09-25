# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    mh_tracking_no = fields.Char(string='MH Tracking No.')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    mh_tracking_no = fields.Char(string='MH Tracking No.', copy=True)


class StockMove(models.Model):
    _inherit = 'stock.move'

    mh_tracking_no = fields.Char(related="picking_id.mh_tracking_no", store=True, readonly=True, string="MH Tracking No.")

    def _get_new_picking_values(self):
        vals = super(StockMove, self)._get_new_picking_values()
        # for sale
        if self.sale_line_id.mh_tracking_no:
            vals['mh_tracking_no'] = self.sale_line_id.mh_tracking_no
        # for Manufacture
        if self.group_id.mh_tracking_no:
            vals['mh_tracking_no'] = self.group_id.mh_tracking_no
        return vals


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    mh_tracking_no = fields.Char(related="move_id.mh_tracking_no", store=True, readonly=True, string="MH Tracking No.")
