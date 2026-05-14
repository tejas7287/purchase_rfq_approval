{
    "name": "RFQ Approval Workflow",
    "version": "1.0",  # Updated to current stable version
    "category": "Inventory/Purchase",  # Standard Odoo category path
    "summary": "Approval workflow for RFQs before Purchase Order confirmation",
    "author": "Internal",
    "license": "LGPL-3",
    "depends": [
        "base",
        "purchase",
        "mail",
        "portal"  # Removed trailing comma
    ],
    "data": [
        "data/mail_templates.xml",
        "security/security.xml",  # Security should usually load BEFORE views
        "security/ir.model.access.csv",

        "views/purchase_approval_team_views.xml",
        "views/purchase_order_views.xml",
        "views/template.xml",  # Portal templates
        "views/menus.xml",  # Removed trailing comma
        # Removed trailing comma
    ],
    "installable": True,
    "application": False,
}
