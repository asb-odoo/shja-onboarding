from odoo import fields, models, _, api
from datetime import datetime


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state_proposal = fields.Selection([
        ('draft', 'Draft'),
        ('send', 'Send'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Cancelled')
    ], string='Proposal_State', index=True,copy=False, default='draft')
    proposal_status = fields.Selection(
        [('not_approved', 'Not Approved'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='not_approved',
        copy=False,
        readonly=True)

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self.state_proposal = 'confirm'
        self.name = self.env['ir.sequence'].next_by_code('sale.order') or _('New')
        return res

    def action_approve(self):
        self.proposal_status = 'approved'
        for rec in self.order_line:
            rec.price_subtotal = rec.proposal_subtotal
            rec.product_uom_qty = rec.accepted_quantity
            rec.price_unit = rec.accepted_price

    def action_reject(self):
        self.proposal_status = 'rejected'
        self.action_cancel()
        self.state_proposal = 'cancel'
        self.name = self.env['ir.sequence'].next_by_code('sale.order') or _('New')

    @api.model
    def create(self, vals):
        if 'company_id' in vals:
            self = self.with_company(vals['company_id'])
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = 'Proposal' + '/' + str(datetime.now().year) + '/' + str(
                datetime.now().strftime('%b')) + '/' + str(
                self.env['ir.sequence'].next_by_code('sale.proposal') or _('New'))

        if any(f not in vals for f in ['partner_invoice_id', 'partner_shipping_id', 'pricelist_id']):
            partner = self.env['res.partner'].browse(vals.get('partner_id'))
            addr = partner.address_get(['delivery', 'invoice'])
            vals['partner_invoice_id'] = vals.setdefault('partner_invoice_id', addr['invoice'])
            vals['partner_shipping_id'] = vals.setdefault('partner_shipping_id', addr['delivery'])
            vals['pricelist_id'] = vals.setdefault('pricelist_id', partner.property_product_pricelist.id)
        result = super(SaleOrder, self).create(vals)
        return result

    def action_quotation_send(self):
        """
        Opens a wizard to compose an email, with relevant mail template loaded by default
        """
        super(SaleOrder, self).action_quotation_send()
        self.state_proposal = 'send'
        self.ensure_one()
        template_id = self._find_mail_template()
        self.env['mail.template'].browse(template_id)
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'mark_so_as_sent': True,
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    accepted_quantity = fields.Integer(string="Accepted Quantity")
    accepted_price = fields.Float(string="Accepted Price")
    proposal_subtotal = fields.Float(string="Proposal Subtotal", compute='_compute_proposal_subtotal')

    @api.depends('accepted_quantity', 'accepted_price', 'tax_id')
    def _compute_proposal_subtotal(self):
        """
        Compute the proposal_subtotal amount of the SO line.
        """
        for line in self:
            taxes = line.tax_id.compute_all(line.accepted_price, line.order_id.currency_id, line.accepted_quantity,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': taxes['total_included'] - taxes['total_excluded'],
                'price_total': taxes['total_included'],
                'proposal_subtotal': taxes['total_excluded'],
            })
            if self.env.context.get('import_file', False) and not self.env.user.user_has_groups(
                    'account.group_account_manager'):
                line.tax_id.invalidate_cache(['invoice_repartition_line_ids'], [line.tax_id.id])
