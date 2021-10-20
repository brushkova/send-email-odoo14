from odoo import models, fields


class SalaryFields(models.Model):
    _name = 'salary.fields'

    first_name = fields.Char(string='Partner first name', required=True)
    last_name = fields.Char(string='Partner last name', required=True)
    salary = fields.Float(string='Partner salary', required=True)
