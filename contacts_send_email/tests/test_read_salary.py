import logging

from odoo.tests.common import TransactionCase, tagged

_logger = logging.getLogger(__name__)


@tagged('-post_install', 'read_salary')
class TestReadSalary(TransactionCase):

    def setUp(self):
        super(TestReadSalary, self).setUp()
        self.sf = self.env['salary.fields']
        self.rsw = self.env['read.salary.wizard']
        self.example_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRQHut43J4idty3-5h7K_G"\
                           "-8nzMpH8jzOvCfpjKU7XSPcK9xgaAxffP5g1Kj88plw0LnQQ_Zj664Csz/pub?output=xlsx"
        self.wizard_1 = self.env['read.salary.wizard'].create({'file_link': self.example_url})

    def test_write_salary_fields(self):
        # check state wizard before run method
        self.assertEqual(self.wizard_1.state, 'step1')
        self.wizard_1.import_xlsx_link()
        # check state wizard after run method
        self.assertEqual(self.wizard_1.state, 'step2')
        # check count line in models
        self.rsw_records = self.rsw.search([])
        self.assertEqual(len(self.rsw_records), 1)
        self.sf_records = self.sf.search([])
        self.assertEqual(len(self.sf_records), 26)
