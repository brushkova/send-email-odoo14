from odoo import api, fields, models


class CollectiveAccount(models.Model):
    _name = 'collective.account'
    _description = 'Collective Account'

    product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True, ondelete='cascade')
    total_product_qty = fields.Integer(string='Total Product QTY', required=True)
    total_product_price = fields.Float(string='Total Product Price', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True, ondelete='cascade')

    @api.model
    def calculate_collective_account(self, partner_id, price_total, product_id, quantity):
        record = self.search([['partner_id', '=', partner_id.id], ['product_id', '=', product_id.id]])

        if record.exists():
            record.total_product_qty = record.total_product_qty + quantity
            record.total_product_price = record.total_product_price + price_total
        else:
            self.create([{
                'partner_id': partner_id.id,
                'total_product_price': price_total,
                'product_id': product_id.id,
                'total_product_qty': quantity
                }
            ])

        return True

    @api.model
    def remove_calculate_collective_account(self, partner_id, price_total, product_id, quantity):
        record = self.search([['partner_id', '=', partner_id.id], ['product_id', '=', product_id.id]])

        if record.exists():
            record.total_product_qty = record.total_product_qty - quantity
            record.total_product_price = record.total_product_price - price_total

        return True
