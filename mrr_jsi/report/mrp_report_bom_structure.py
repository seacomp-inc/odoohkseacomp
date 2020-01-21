# -*- coding: utf-8 -*-

import json

from odoo import api, models, _
from odoo.tools import float_round

class ReportBomMaterial(models.AbstractModel):
    _name = 'report.mrr_jsi.report_bom_material_rediness'
    _description = 'BOM Material Readiness Report'

    @api.model
    def get_html(self, bom_id=False, searchQty=1, searchVariant=False, related_pol=False):
        res = self._get_report_data(bom_id=bom_id, searchQty=searchQty, searchVariant=searchVariant)
        res['lines']['report_type'] = 'html'
        res['lines']['report_structure'] = 'all'
        if related_pol:
            related_pol = related_pol
        else:
            related_pol = res['lines']['related_pol']
        for component in res['lines']['components']:
            for i in component['related_pol']:
                related_pol.append(i)
            if component['child_bom']:
                self.get_html(bom_id=component['child_bom'], related_pol=related_pol)

        res['lines']['related_pol'] = related_pol
        res['lines'] = self.env.ref('mrr_jsi.report_bom_material_rediness').render({'data': res['lines']})
        return res

    @api.model
    def get_bom(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
        lines = self._get_bom(bom_id=bom_id, product_id=product_id, line_qty=line_qty, line_id=line_id, level=level)
        return self.env.ref('mrr_jsi.report_mrp_bom_material_line').render({'data': lines})

    def _get_bom_reference(self, bom):
        return bom.display_name

    @api.model
    def _get_report_data(self, bom_id, searchQty=0, searchVariant=False):
        lines = {}
        bom = self.env['mrp.bom'].browse(bom_id)
        bom_quantity = searchQty or bom.product_qty
        bom_product_variants = {}
        bom_uom_name = ''

        if bom:
            bom_uom_name = bom.product_uom_id.name

            # Get variants used for search
            if not bom.product_id:
                for variant in bom.product_tmpl_id.product_variant_ids:
                    bom_product_variants[variant.id] = variant.display_name

        lines = self._get_bom(bom_id, product_id=searchVariant, line_qty=bom_quantity, level=1)
        return {
            'lines': lines,
            'variants': bom_product_variants,
            'bom_uom_name': bom_uom_name,
            'bom_qty': bom_quantity,
            'is_variant_applied': self.env.user.user_has_groups('product.group_product_variant') and len(bom_product_variants) > 1,
            'is_uom_applied': self.env.user.user_has_groups('uom.group_uom')
        }

    def _get_bom(self, bom_id=False, product_id=False, line_qty=False, line_id=False, level=False):
        bom = self.env['mrp.bom'].browse(bom_id)
        bom_quantity = line_qty
        if line_id:
            current_line = self.env['mrp.bom.line'].browse(int(line_id))
            bom_quantity = current_line.product_uom_id._compute_quantity(line_qty, bom.product_uom_id)
        # Display bom components for current selected product variant
        if product_id:
            product = self.env['product.product'].browse(int(product_id))
        else:
            product = bom.product_id or bom.product_tmpl_id.product_variant_id
        if not product:
            product = bom.product_tmpl_id
        lines = {
            'bom': bom,
            'bom_qty': bom_quantity,
            'bom_prod_name': product.display_name,
            'currency': self.env.user.company_id.currency_id,
            'product': product,
            'code': bom and self._get_bom_reference(bom) or '',
            'level': level or 0,
        }
        components = self._get_bom_lines(bom, bom_quantity, product, line_id, level)
        lines['components'] = components

        # Quantity On Order
        pol = self.env['purchase.order.line'].search([
            ('product_id', '=', product.id),
            ('state', 'in', ['purchase']),
        ])
        quantity_on_order = 0.00
        for line in pol:
            quantity_on_order += (line.product_qty - line.qty_received)

        # Quantity On Hand
        quantity_on_hand = product.qty_available

        lines['related_pol'] = pol.ids
        lines['quantity_on_hand'] = quantity_on_hand
        lines['quantity_on_order'] = quantity_on_order

        return lines

    def _get_bom_lines(self, bom, bom_quantity, product, line_id, level):
        components = []
        for line in bom.bom_line_ids:
            line_quantity = (bom_quantity / (bom.product_qty or 1.0)) * line.product_qty
            if line._skip_bom_line(product):
                continue
            components.append({
                'prod_id': line.product_id.id,
                'prod_name': line.product_id.display_name,
                'code': line.child_bom_id and self._get_bom_reference(line.child_bom_id) or '',
                'prod_qty': line_quantity,
                'prod_uom': line.product_uom_id.name,
                'parent_id': bom.id,
                'line_id': line.id,
                'level': level or 0,
                'child_bom': line.child_bom_id.id,
                'phantom_bom': line.child_bom_id and line.child_bom_id.type == 'phantom' or False,
            })
        for line in components:
            product = self.env['product.product'].browse(line['prod_id'])
            
            # Quantity On Order
            pol = self.env['purchase.order.line'].search([
                ('product_id', '=', product.id),
                ('state', 'in', ['purchase']),
            ])
            quantity_on_order = 0.00
            for line1 in pol:
                quantity_on_order += (line1.product_qty - line1.qty_received)

            # Quantity On Hand
            quantity_on_hand = product.qty_available
            line.update({'quantity_on_hand': quantity_on_hand, 'quantity_on_order': quantity_on_order, 'related_pol': pol.ids})
        return components
