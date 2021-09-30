from odoo import api, fields, models, _


class Partner(models.Model):
    _inherit = 'res.partner'

    country_code = fields.Char(related='country_id.code')

    @api.model_create_multi
    def create(self, vals_list):
        partners = super(Partner, self).create(vals_list)
        for partner in partners:
            partner._send_mail()

        return partners

    def write(self, vals):
        result = super(Partner, self).write(vals)
        if vals.get('email'):
            self._send_mail()

        return result

    def _send_mail(self):
        self.message_post(body='Welcome, %s. Have a nice day!' % self.name)

        if self.email:
            mail = self.env['mail.mail'].sudo().create([{
                'subject': _('Login notification %s') % self.name,
                'email_from': 'brushkovak@gmail.com',
                'email_to': self.email,
                'body_html': '<p>Your account was successfully created or email changed<p/>',
            }])
            mail.send()
            return True

        return False
