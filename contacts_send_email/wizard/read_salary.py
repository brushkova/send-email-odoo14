import base64
import csv
import io

import requests
import xlrd

from odoo import models, fields


class ReadSalaryWizard(models.TransientModel):
    _name = 'read.salary.wizard'

    file_salary = fields.Binary(string='Salary File', help='Upload file')
    file_link = fields.Char(string='Link file', help='Unload link')
    state = fields.Selection(selection=[('step1', 'step1'), ('step2', 'step2')], default='step1')
    count = fields.Integer()

    def import_csv_file(self):
        csv_data = base64.b64decode(self.file_salary)
        data_file = io.StringIO(csv_data.decode("utf-8"))
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
        r = requests.get(self.file_link)  # make an HTTP request
        book = xlrd.open_workbook(file_contents=r.content)  # access the response body as bytes
        sheet = book.sheet_by_index(0)

        name_col = ['first_name', 'last_name', 'salary']
        col_value = []
        for row in range(sheet.nrows):
            self.count += 1
            elm = {}
            for col in range(sheet.ncols):
                elm[name_col[col]] = sheet.cell_value(row, col)
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
