# -*- coding: utf-8 -*-

from odoo import models, fields, api

class mhPartners(models.Model):
    _inherit = 'res.partner' 
    _sql_constraints = [
     ('name','unique(name)','*** NAME must be unique! ***')
    ]

    
    @api.multi
    def _purchase_invoice_count(self):
        PurchaseOrder = self.env['purchase.order']
        Invoice = self.env['account.invoice']
        for partner in self:
            partner.purchase_order_count = PurchaseOrder.search_count([('partner_id', 'child_of', partner.id)])
            partner.supplier_invoice_count = Invoice.search_count([('partner_id', 'child_of', partner.id), ('type', '=', 'in_invoice')])

#    def _compute_sale_order_count(self):
#        sale_data = self.env['sale.order'].read_group(domain=[('partner_id', 'child_of', self.ids)],
#                                                      fields=['partner_id'], groupby=['partner_id'])
#        # read to keep the child/parent relation while aggregating the read_group result in the loop
#        partner_child_ids = self.read(['child_ids'])
#        mapped_data = dict([(m['partner_id'][0], m['partner_id_count']) for m in sale_data])
#        for partner in self:
#            # let's obtain the partner id and all its child ids from the read up there
#            partner_ids = filter(lambda r: r['id'] == partner.id, partner_child_ids)[0]
#            partner_ids = [partner_ids.get('id')] + partner_ids.get('child_ids')
#            # then we can sum for all the partner's child
#            partner.sale_order_count = sum(mapped_data.get(child, 0) for child in partner_ids)

    def _compute_issued_total(self):
        """ Returns the issued total as will be displayed on partner view """
        today = fields.Date.context_today(self)
        domain = self.get_followup_lines_domain(today, overdue_only=True)
        for aml in self.env['account.move.line'].search(domain):
            aml.partner_id.issued_total += aml.amount_residual
            
# Add new fields for Contacts/Partners

    purchase_order_count = fields.Integer(compute='_purchase_invoice_count', string="# of Purchase Order")
    sale_order_count = fields.Integer(compute='_compute_sale_order_count', string="# of Sales Order")
    cny_name = fields.Char(string="Chinese Name", store='True')
    manufacturer = fields.Boolean(string="Is a Manufacturer", store='True', default='False')
    short_name = fields.Char(string="Short name", store='True')
    vendor_code = fields.Char(string="Vendor Code", store='True')
    issued_total = fields.Monetary(compute='_compute_issued_total', string="Journal Items 2")
    fax = fields.Char(string="Fax", store='True')