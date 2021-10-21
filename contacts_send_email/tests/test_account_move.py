from odoo.tests import TransactionCase, tagged


@tagged('-post_install', 'chek_invoice')
class TestAccountMove(TransactionCase):

    def setUp(self):
        super(TestAccountMove, self).setUp()
        self.partner_1 = self.env['res.partner'].create({'name': "Test User"})
        self.partner_2 = self.env['res.partner'].create({'name': "Test User 2"})
        self.product_1 = self.env['product.product'].create({
            'name': 'Test Product'
        })
        self.ca = self.env['collective.account']
        self.invoice_1 = self.env['account.move'].create({
            'unload_calculate_invoice': True,
            'move_type': 'out_invoice',
            'partner_id': self.partner_1.id,
            'invoice_line_ids': [(0, 0, {
                'name': self.product_1.name,
                'quantity': 1,
                'price_unit': 10,
                'product_id': self.product_1.id
            })]

        })
        self.invoice_2 = self.env['account.move'].create({
            'unload_calculate_invoice': True,
            'move_type': 'out_invoice',
            'partner_id': self.partner_1.id,
            'invoice_line_ids': [(0, 0, {
                'name': self.product_1.name,
                'quantity': 2,
                'price_unit': 10,
                'product_id': self.product_1.id
            })]
        })
        self.invoice_3 = self.env['account.move'].create({
            'unload_calculate_invoice': True,
            'move_type': 'out_invoice',
            'partner_id': self.partner_2.id,
            'invoice_line_ids': [(0, 0, {
                'name': self.product_1.name,
                'quantity': 4,
                'price_unit': 10,
                'product_id': self.product_1.id
            })]
        })

    def test_create_collective_account(self):
        # check invoice_1 state and count before
        self.assertEqual(self.invoice_1.state, 'draft')
        self.assertEqual(self.ca.search_count([]), 0)
        # check invoice_1 after press 'confirm' button
        self.invoice_1.action_post()
        self.ca_record_1 = self.ca.search([
            ('partner_id', '=', self.partner_1.id),
            ('product_id', '=', self.product_1.id)
        ])
        self.assertEqual(self.invoice_1.state, 'posted')
        self.assertEqual(self.ca_record_1.total_product_qty, 1)
        self.assertEqual(self.ca_record_1.total_product_price, 10)
        self.assertEqual(len(self.ca_record_1), 1)
        # check invoice_2 after press 'confirm' button
        self.invoice_2.action_post()
        self.assertEqual(self.invoice_2.state, 'posted')
        self.assertEqual(self.ca_record_1.total_product_qty, 3)
        self.assertEqual(self.ca_record_1.total_product_price, 30)
        self.assertEqual(len(self.ca_record_1), 1)
        # check invoice_3 after press 'confirm' button
        self.invoice_3.action_post()
        self.ca_record_2 = self.ca.search([
            ('partner_id', '=', self.partner_2.id),
            ('product_id', '=', self.product_1.id)
        ])
        self.assertEqual(self.invoice_3.state, 'posted')
        self.assertEqual(self.ca_record_2.total_product_qty, 4)
        self.assertEqual(self.ca_record_2.total_product_price, 40)
        # check invoices lines
        self.assertEqual(len(self.ca_record_1), 1)
        self.assertEqual(len(self.ca_record_2), 1)
        self.assertEqual(self.ca.search_count([]), 2)
        # check invoice_1 after press 'reset to draft' button
        self.invoice_1.button_draft()
        self.assertEqual(self.invoice_1.state, 'draft')
        self.assertEqual(self.ca_record_1.total_product_qty, 2)
        self.assertEqual(self.ca_record_1.total_product_price, 20)
        self.assertEqual(len(self.ca_record_1), 1)
        self.assertEqual(self.ca.search_count([]), 2)
        # check invoice_2 after press 'reset to draft' button
        self.invoice_2.button_draft()
        self.assertEqual(self.invoice_2.state, 'draft')
        self.assertEqual(self.ca_record_1.total_product_qty, 0)
        self.assertEqual(self.ca_record_1.total_product_price, 0)
        self.assertEqual(self.ca.search_count([]), 2)
        # check invoice_3 after press 'reset to draft' button
        self.invoice_3.button_draft()
        self.assertEqual(self.invoice_3.state, 'draft')
        self.assertEqual(self.ca_record_2.total_product_qty, 0)
        self.assertEqual(self.ca_record_2.total_product_price, 0)
        self.assertEqual(len(self.ca_record_2), 1)
        self.assertEqual(self.ca.search_count([]), 2)
