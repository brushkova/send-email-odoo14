import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class CollectiveAccount(models.Model):
    _name = "collective.account"
    _description = "Collective Account"

    product_id = fields.Many2one(comodel_name='product.product', string='Product', required=True, ondelete='cascade')
    total_product_qty = fields.Integer(string="Total Product QTY", required=True)
    total_product_price = fields.Float(string="Total Product Price", required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', string='Partner', required=True, ondelete='cascade')
    invoice_id = fields.Text(name="Name", required=True)

    @api.model
    def _create_collective_account(self, invoice_id, partner_id, product_id, quantity, price_total):
        record = self.search([('partner_id', '=', partner_id.id), ('product_id', '=', product_id.id)])

        if record.exists():
            if record.invoice_id != invoice_id:
                record.total_product_qty = record.total_product_qty + quantity
                record.total_product_price = record.total_product_price + price_total
        else:
            self.create([{
                'invoice_id': invoice_id,
                'partner_id': partner_id.id,
                'product_id': product_id.id,
                'total_product_qty': quantity,
                'total_product_price': price_total
                }
            ])

        return True
