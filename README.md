# RFQ Approval Workflow

**Version:** 1.0  
**Category:** Inventory/Purchase  
**License:** LGPL-3  
**Author:** Internal

## Description

Approval workflow for RFQs before Purchase Order confirmation

## Features

- Odoo 19.0 compatible
- Addon module
- Approval workflow for RFQs before Purchase Order confirmation

## Dependencies

This module depends on the following Odoo modules:

- `base`
- `purchase`
- `mail`
- `portal`

## Installation

1. Clone this repository into your Odoo addons directory:
   ```bash
   git clone https://github.com/tejas7287/purchase_rfq_approval.git
   ```

2. Add the module path to your Odoo configuration file (`odoo.conf`):
   ```
   addons_path = /path/to/odoo/addons,/path/to/purchase_rfq_approval
   ```

3. Restart the Odoo server:
   ```bash
   sudo systemctl restart odoo
   ```

4. Go to **Apps** → **Update Apps List** → Search for **"RFQ Approval Workflow"** → Click **Install**

## Module Structure

```
purchase_rfq_approval/
├── __init__.py
├── __manifest__.py
├── controllers/
├── data/
├── models/
├── security/
├── views/
```

## Configuration

After installation, configure the module through Odoo's Settings menu or the module's specific configuration options.

## License

This project is licensed under the LGPL-3 License.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request
