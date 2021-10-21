from odoo.tests.common import TransactionCase, tagged


@tagged('-post_install', 'read_salary')
class TestReadSalary(TransactionCase):

    def setUp(self):
        super(TestReadSalary, self).setUp()
        self.sf = self.env['salary.fields']
        self.rsw = self.env['read.salary.wizard']
        self.wizard_1 = self.env['read.salary.wizard'].create({'link_xlsx': "https://docs.google.com/spreadsheets/d/"
                                                                            "e/2PACX-1vRQHut43J4idty3-5h7K_G-8nzMpH8jz"
                                                                            "OvCfpjKU7XSPcK9xgaAxffP5g1Kj88plw0LnQQ_Zj6"
                                                                            "64Csz/pub?output=xlsx"})

    def test_write_salary_fields(self):
        # check state wizards before run method
        self.assertEqual(self.wizard_1.state, 'step1')
        self.wizard_1.import_xlsx_link()
        # check state wizards after run method
        self.assertEqual(self.wizard_1.state, 'step2')
        # check count line in models
        self.sf_records = self.sf.search([])
        self.assertEqual(len(self.sf_records), 26)
        self.sf_record_fn = self.sf.search([
            ('first_name', '=', 'Kate'),
        ])
        self.assertEqual(len(self.sf_record_fn), 5)
