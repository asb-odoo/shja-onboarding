from odoo import models, fields, api


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    second_discount = fields.Float(string="2nd Disc. %")
    currency_id = fields.Many2one(comodel_name='res.currency', string='currency')
    price_subtotal = fields.Monetary(currency_field='currency_id', string='price total', store=True,
                                     compute='_compute_amount')

    @api.depends('product_template_id', 'product_uom_qty', 'discount', 'price_unit', 'tax_id', 'second_discount')
    def _compute_amount(self):
        res = super(SaleOrderLine, self)._compute_amount()
        for rec in self:
            if rec.second_discount:
                rec.price_subtotal = (rec.price_subtotal - rec.price_subtotal * (rec.second_discount / 100))
        return res

    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        if res:
            res['second_discount'] = self.second_discount
        return res

