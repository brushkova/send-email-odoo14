{
    "name": "Contacts Send Email",
    "version": "14.0.1.0.0",
    "depends": [
        "account",
        "base",
        "contacts",
        "mail",
        "sale_management",
        "stock",
    ],
    "author": "Kate Brushkova",
    "summary": "After creating a new contact, a message will be send to email.",
    "website": "https://www.example.com",
    'category': "uncategory",
    "sequence": 5,
    "data": [
        "security/ir.model.access.csv",
        "views/contacts_send_email_view.xml",
        "views/seq_sale_order.xml",
        "views/collective_account_view.xml",
        "views/view_move_form.xml",
        "wizards/read_salary_view.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False
}
