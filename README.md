# RFQ Approval Workflow

![Version](https://img.shields.io/badge/version-1.0-blue)
![Category](https://img.shields.io/badge/category-Inventory%2FPurchase-green)
![License](https://img.shields.io/badge/license-LGPL-3-orange)

| | |
|---|---|
| **Name** | RFQ Approval Workflow |
| **Version** | 1.0 |
| **Category** | Inventory/Purchase |
| **Author** | Internal |
| **License** | LGPL-3 |
| **Application** | No (Addon) |

## Description

Approval workflow for RFQs before Purchase Order confirmation

## Functionality

### Models & Fields

#### `purchase.approval.history` — Purchase Approval History

**File:** `models/purchase_approval_history.py`

**Fields:**

| Field | Type |
|-------|------|
| `order_id` | `Many2one` |
| `user_id` | `Many2one` |
| `action` | `Selection` |
| `remark` | `Text` |

#### `purchase.approval.rule` — Purchase Approval Rule

**File:** `models/purchase_approval_rule.py`

**Fields:**

| Field | Type |
|-------|------|
| `team_id` | `Many2one` |
| `sequence` | `Integer` |
| `min_amount` | `Monetary` |
| `max_amount` | `Monetary` |
| `approver_ids` | `Many2many` |
| `currency_id` | `Many2one` |

#### `purchase.approval.team` — Purchase Approval Team

**File:** `models/purchase_approval_team.py`

**Fields:**

| Field | Type |
|-------|------|
| `name` | `Char` |
| `company_id` | `Many2one` |
| `rule_ids` | `One2many` |

#### Extends `purchase.order`

**File:** `models/purchase_order.py`

**Inherits:** `purchase.order`

**Fields:**

| Field | Type |
|-------|------|
| `approval_team_id` | `Many2one` |
| `technical_team_id` | `Many2one` |
| `state` | `Selection` |
| `approval_state` | `Selection` |
| `approval_history_ids` | `One2many` |
| `pr_id` | `Many2one` |
| `vendor_decision` | `Selection` |
| `vendor_decision_date` | `Date` |
| `vendor_reject_reason` | `Text` |
| `is_pr_based` | `Boolean` |

**Key Methods:**

- `_compute_is_pr_based()` — Computed field
- `action_submit_for_approval()` — Action/workflow method
- `action_submit_for_approval()` — Action/workflow method
- `action_approve()` — Action/workflow method
- `action_approve()` — Action/workflow method
- `action_approve()` — Action/workflow method
- `button_confirm()` — Button handler
- `button_confirm()` — Button handler
- `create()` — Overridden ORM method
- `action_reject()` — Action/workflow method

### Views & UI

**Form Views:** `purchase_approval_team_views.xml`, `template.xml`

**List/Tree Views:** `purchase_approval_team_views.xml`, `purchase_order_views.xml`

**Menus:** `menus.xml`

**Website/Portal Templates:**

- `purchase.portal_my_purchase_order` (`template.xml`)

### Security

**Security Groups:**

- Purchase Approver

**Access Rights:** 4 model access rules defined

| Model |
|-------|
| `Purchase Approval Team` |
| `Purchase Approval Rule` |
| `Purchase Approval History User` |
| `Purchase Approval History Approver` |

### Web Controllers & Routes

| Route | Controller |
|-------|------------|
| `/my/purchase/<int:order_id>/acknowledge` | `portal.py` |

### Data & Automation

**Email Templates:** `mail_templates.xml`

## Dependencies

| Module | Type |
|--------|------|
| `base` | Odoo Core |
| `purchase` | Odoo Core |
| `mail` | Odoo Core |
| `portal` | Odoo Core |

## File Structure

```
purchase_rfq_approval/
├── LICENSE
├── README.md
├── __init__.py
├── __manifest__.py
├── controllers/
│   ├── __init__.py
│   └── portal.py
├── data/
│   └── mail_templates.xml
├── models/
│   ├── __init__.py
│   ├── purchase_approval_history.py
│   ├── purchase_approval_rule.py
│   ├── purchase_approval_team.py
│   └── purchase_order.py
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
└── views/
    ├── menus.xml
    ├── purchase_approval_team_views.xml
    ├── purchase_order_views.xml
    └── template.xml
```

## Installation

This module is part of the **[odoo-purchase-vendor-suite](https://github.com/tejas7287/odoo-purchase-vendor-suite)** suite.

1. Place this module in your Odoo addons directory
2. Update the apps list: **Settings** → **Apps** → **Update Apps List**
3. Search for **"RFQ Approval Workflow"** and click **Install**

## License

LGPL-3
