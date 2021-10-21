import base64
import csv
import io
import os

import requests
import xlrd


from odoo import fields, models
from odoo.exceptions import UserError
from requests.exceptions import MissingSchema


class ReadSalaryWizard(models.TransientModel):
    _name = 'read.salary.wizard'

    file_csv = fields.Binary(string='Unload .csv File', help='Upload file')
    file_name = fields.Char(string='File Name')
    link_xlsx = fields.Char(string='Insert .xlsx Link', help='Unload link')
    state = fields.Selection(selection=[('step1', 'step1'), ('step2', 'step2')], default='step1')
    count = fields.Integer()

    def import_csv_file(self):
        csv_data = base64.b64decode(self.file_csv)
        ext = os.path.splitext(self.file_name)[-1].lower()
        if ext != '.csv':
            raise UserError('Only csv files are supported.')

        try:
            data_file = io.StringIO(csv_data.decode("utf-8"))
        except ValueError:
            raise UserError('Only csv files are supported.')
        csv_reader = csv.DictReader(data_file, delimiter=',')

        data = []
        for row in csv_reader:
            self.count += 1
            data.append({
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'salary': float(row['salary'])
            })
            if len(data) == 10:
                self.env['salary.fields'].create(data)
                data.clear()
        if data:
            self.env['salary.fields'].create(data)

        self.write({'state': 'step2'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'read.salary.wizard',
            'view_mode': 'form',
            'binding_view_types': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }

    def import_xlsx_link(self):
        try:
            r = requests.get(self.link_xlsx)  # make an HTTP request
            if r.status_code != 200:
                raise UserError('Only excel files are supported.')
        except MissingSchema:
            raise UserError('Only excel files are supported.')

        try:
            book = xlrd.open_workbook(file_contents=r.content)  # access the response body as bytes
        except xlrd.biffh.XLRDError:
            raise UserError('Only excel files are supported.')

        sheet = book.sheet_by_index(0)
        col_value = []
        for row in range(sheet.nrows):
            self.count += 1
            elm = dict(zip(['first_name', 'last_name', 'salary'], sheet.row_values(row)))

            col_value.append(elm)
            if len(col_value) == 10:
                self.env['salary.fields'].create(col_value)
                col_value.clear()

        if col_value:
            self.env['salary.fields'].create(col_value)

        self.write({'state': 'step2'})
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'read.salary.wizard',
            'view_mode': 'form',
            'binding_view_types': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }
