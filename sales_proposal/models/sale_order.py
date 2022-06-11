from odoo import fields, models, _, api
from datetime import datetime


class SaleOrder(models.Model):
    _inherits = ['sale.order','sale.order.line']

    state_proposal = fields.Selection([
        ('draft', 'Draft'),
        ('send', 'Send'),
        ('confirm', 'Confirm')
    ], string='Proposal_State', copy=False, index=True, default='draft')
    proposal_status = fields.Selection(
        [('not_approved', 'Not Approved'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='not_approved',
        readonly=True)
    accepted_quantity = fields.Integer(string="Accepted Quantity")
    accepted_price = fields.Float(string="Accepted Price")

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        print("res",res)
        return res

    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            self = self.with_company(vals['company_id'])
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = 'Proposal' + '/' + str(datetime.now().year) + '/' + str(datetime.now().strftime('%b')) + '/' + str(self.env['ir.sequence'].next_by_code('sale.proposal') or _('New'))

        # Makes sure partner_invoice_id', 'partner_shipping_id' and 'pricelist_id' are defined
        if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            addr = partner.address_get(['delivery', 'invoice'])
            vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
            vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
            vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist.id)
        result = super(SaleOrder, self).create(vals)
        return result
