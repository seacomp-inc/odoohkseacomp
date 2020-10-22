# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    mh_tracking_no = fields.Char(string='MH Tracking No.', copy=True)

    @api.model
    def create(self, values):
        if not values.get('name', False) or values['name'] == _('New'):
            picking_type_id = values.get('picking_type_id') or self._get_default_picking_type()
            picking_type_id = self.env['stock.picking.type'].browse(picking_type_id)
            if picking_type_id:
                values['name'] = picking_type_id.sequence_id.next_by_id()
            else:
                values['name'] = self.env['ir.sequence'].next_by_code('mrp.production') or _('New')
        if not values.get('procurement_group_id'):
            # values['procurement_group_id'] = self.env["procurement.group"].create({'name': values['name']}).id
            # by jsi
            values['procurement_group_id'] = self.env["procurement.group"].create({'mh_tracking_no': values.get('mh_tracking_no'), 'name': values.get('name')}).id
        production = super(MrpProduction, self).create(values)
        return production

    @api.one
    def button_transfer_details(self):
        if self.picking_ids and self.mh_tracking_no:
            self.picking_ids.write({'mh_tracking_no': self.mh_tracking_no})

    # @api.model
    # def create(self, values):
    #     production = super(MrpProduction, self).create(values)
    #     print(stop2)
    #     production.procurement_group_id.mh_tracking_no = values.get('mh_tracking_no', '')
    #     return production

class StockMove(models.Model):
    _inherit = 'stock.move'

    mo_mh_tracking_no = fields.Char(related="raw_material_production_id.mh_tracking_no", store=True, readonly=True, string="MH Tracking No.(MO)")


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    mo_mh_tracking_no = fields.Char(related="move_id.production_id.mh_tracking_no", store=True, readonly=True, string="MH Tracking No.(MO)")
