from odoo import fields, models, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    second_discount = fields.Float(string='2nd Disc. %')

    # @api.model
    # def create(self, vals):
    #     print("\n account move line ====", self, vals)
    #     res = super(AccountMoveLine, self).create(vals)
    #     print("\n ressssss====>>>>>>>>", res)
    #     return res


    # @api.onchange('second_discount')
    # def _onchange_second_discount(self):
    #     for line in self:
    #         print("line1",line.price_subtotal)
    #         print("line2",line.second_discount)
    #         line.price_subtotal = (line.price_subtotal - line.price_subtotal * (line.second_discount / 100))

    @api.model
    def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes, move_type):
        res = super(AccountMoveLine, self)._get_price_total_and_subtotal_model(price_unit, quantity, discount, currency, product, partner, taxes, move_type)
        for rec in self:
            if rec.second_discount and discount:
                print("previous total",rec.price_subtotal,rec.second_discount)
                print("self discount previous")
                rec['price_subtotal'] = (rec.price_subtotal - rec.price_subtotal * (rec.second_discount / 100))
                print("After Subtotal",rec.price_subtotal,rec.second_discount)
        return res

    # @api.model
    # def _get_price_total_and_subtotal_model(self, price_unit, quantity, discount, currency, product, partner, taxes, move_type):
    #     print("==========",self)
    #     res = super(AccountMoveLine,self)._get_price_total_and_subtotal_model(price_unit,quantity,discount,currency,product,partner,taxes,move_type)
    #     print("===============",res)
    #     print("===========",self.second_discount)
    #     if self.second_discount:
    #             res['price_subtotal'] = (self.price_subtotal - self.price_subtotal * (self.second_discount / 100))
    #     print("=====2======",res)
    #     return  res

    # @api.onchange('quantity', 'discount', 'price_unit', 'tax_ids','second_discount')
    # def _onchange_price_subtotal(self):
    #     res = super(AccountMoveLine,self)._onchange_price_subtotal()
    #     for line in self:
    #         print("===========",line)
    #         if line.second_discount and line.price_subtotal:
    #             line.price_subtotal = (line.price_subtotal - line.price_subtotal * (line.second_discount / 100))
    #             print("second_discount",line.second_discount)
    #             print("Price Subtotal",line.price_subtotal)
    #         line.update(line._get_price_total_and_subtotal())
    #         line.update(line._get_fields_onchange_subtotal())
    #         line._onchange_second_discount()
    #
    #     return res