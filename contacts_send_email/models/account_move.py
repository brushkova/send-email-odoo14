import logging

from odoo import models

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    def _post(self, soft=True):
        to_post = super()._post(soft=soft)

        for move in to_post:

            for line in move.line_ids.filtered(
                    lambda i: i.exclude_from_invoice_tab is False and i.product_id.type in ['consu', 'product']):

                self.env['collective.account']._create_collective_account(move.invoice_origin,
                                                                          move.commercial_partner_id,
                                                                          line.product_id,
                                                                          line.quantity,
                                                                          line.price_total
                                                                          )
        return to_post
