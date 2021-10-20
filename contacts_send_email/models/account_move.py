from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    unload_calculate_invoice = fields.Boolean(string='Unload Calculate Invoice')

    def _post(self, soft=True):
        to_post = super(AccountMove, self)._post(soft=soft)

        for move in to_post:
            if move.unload_calculate_invoice is True:
                for line in move.line_ids.filtered(
                        lambda i: i.exclude_from_invoice_tab is False
                        and i.product_id.type in ['consu', 'product']
                ):
                    self.env['collective.account'].calculate_collective_account(
                        move.commercial_partner_id,
                        line.price_total,
                        line.product_id,
                        line.quantity
                    )
        return to_post

    def button_draft(self):
        res = super(AccountMove, self).button_draft()

        for move in self:
            if move.unload_calculate_invoice is True:
                for line in move.line_ids.filtered(
                        lambda i: i.exclude_from_invoice_tab is False
                        and i.product_id.type in ['consu', 'product']
                ):
                    self.env['collective.account'].remove_calculate_collective_account(
                        move.commercial_partner_id,
                        line.price_total,
                        line.product_id,
                        line.quantity
                    )

        return res
