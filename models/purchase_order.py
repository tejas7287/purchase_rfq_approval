from odoo import models, fields,api
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    approval_team_id = fields.Many2one(
        "purchase.approval.team",
        string="Approval Team",tracking=True
    )
#NEW CODE ADDED
    technical_team_id = fields.Many2one(
        'purchase.approval.team',  # MASTER MODEL
        string="Technical Team Approval",
        required=False
    )
    # state = fields.Selection(
    #     selection_add=[
    #         ('vendor_pending', 'Vendor Pending'),
    #         ('vendor_accepted', 'Vendor Accepted'),
    #         ('vendor_rejected', 'Vendor Rejected'),
    #     ]
    # )

    approval_state = fields.Selection(
        [
            ("draft", "Draft"),
            ("to_approve", "Waiting Approval"),
            ("approved", "Approved"),
            ("rejected", "Rejected"),
        ],
        default="draft",
        tracking=True
    )

    approval_history_ids = fields.One2many(
        "purchase.approval.history",
        "order_id",
        string="Approval History",tracking=True
    )

    pr_id = fields.Many2one(
        "material.purchase.requisition",
        string="Purchase Requisition",
        readonly=True,
        index=True,
        ondelete="set null",tracking=True
    )


    vendor_decision = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string="Vendor Decision",tracking=True)
    vendor_decision_date = fields.Date(string="Vendor Decision Date",tracking=True)
    vendor_reject_reason = fields.Text(string="Vendor Reject Reason",tracking=True)

    is_pr_based = fields.Boolean(
        compute="_compute_is_pr_based",
        store=True,tracking=True
    )

    def _compute_is_pr_based(self):
        for order in self:
            order.is_pr_based = bool(order.pr_id)

    def action_submit_for_approval(self):

        for order in self:

            if not order.pr_id:
                raise UserError("Approval only for PR RFQs.")

            if not order.approval_team_id:
                raise UserError("Please select Approval Team.")

            order.approval_state = "to_approve"

            # Create approval history
            self.env["purchase.approval.history"].sudo().create({
                "order_id": order.id,
                "user_id": self.env.user.id,
                "action": "submitted",
            })

            # Load mail template
            template = self.env.ref(
                "purchase_rfq_approval.mail_template_po_submit_approval",
                raise_if_not_found=False
            )

            if not template:
                _logger.warning("Mail template not found!")
                return

            # Get approvers with email
            approvers = order.approval_team_id.rule_ids.mapped(
                "approver_ids"
            ).filtered(lambda u: u.email)

            if not approvers:
                _logger.warning("No approvers with email found.")
                return

            # Combine emails
            email_to = ",".join(approvers.mapped("email"))

            # Send mail
            template.sudo().send_mail(
                order.id,
                force_send=True,
                email_values={
                    "email_to": email_to
                }
            )


    # def action_submit_for_approval(self):
    #     for order in self:
    #         if not order.approval_team_id:
    #             raise UserError("Please select an Approval Team.")
    #
    #         order.approval_state = "to_approve"
    #
    #         self.env["purchase.approval.history"].sudo().create({
    #             "order_id": order.id,
    #             "user_id": self.env.user.id,
    #             "action": "submitted",
    #         })
    def action_approve(self):
        for order in self:

            # 🔥 ADMIN FULL APPROVAL (ADD HERE)
            if self.env.user.has_group('base.group_system'):
                self.env["purchase.approval.history"].sudo().create({
                    "order_id": order.id,
                    "user_id": self.env.user.id,
                    "action": "approved",
                })

                order.approval_state = "approved"

                continue  # ⭐ VERY IMPORTANT
            rules = order.approval_team_id.rule_ids.filtered(
                    lambda r: r.min_amount <= order.amount_total <= r.max_amount
                )

            if not rules or self.env.user not in rules.approver_ids:
                    raise UserError("You are not authorized to approve this RFQ.")

            self.env["purchase.approval.history"].sudo().create({
                "order_id": order.id,
                "user_id": self.env.user.id,
                "action": "approved",
            })

            order.approval_state = "approved"

    # def action_approve(self):
    #     for order in self:
    #         rules = order.approval_team_id.rule_ids.filtered(
    #             lambda r: r.min_amount <= order.amount_total <= r.max_amount
    #         )
    #
    #         # if not rules or self.env.user not in rules.approver_ids:
    #         #     raise UserError("You are not authorized to approve this RFQ.")
    #
    #
    #         self.env["purchase.approval.history"].sudo().create({
    #             "order_id": order.id,
    #             "user_id": self.env.user.id,
    #             "action": "approved",
    #         })
    #
    #         order.approval_state = "approved"
            # ✅ DO NOT TOUCH order.state

    # def action_approve(self):
    #     for order in self:
    #         rules = order.approval_team_id.rule_ids.filtered(
    #             lambda r: r.min_amount <= order.amount_total <= r.max_amount
    #         )
    #
    #         if not rules or self.env.user not in rules.approver_ids:
    #             raise UserError("You are not authorized to approve this RFQ.")
    #
    #         self.env["purchase.approval.history"].sudo().create({
    #             "order_id": order.id,
    #             "user_id": self.env.user.id,
    #             "action": "approved",
    #         })
    #
    #         order.approval_state = "approved"
    #         order.state = "vendor_pending"  # 🔑 THIS LINE

    def button_confirm(self):
        for order in self:
            # if order.pr_id:
            if order.pr_id and not self.env.user.has_group('base.group_system'):
                if order.approval_state != "approved":
                    raise UserError("RFQ must be approved before confirmation.")

                if order.vendor_decision != "yes":
                    raise UserError("Vendor has not accepted the RFQ.")

        return super().button_confirm()

    # def button_confirm(self):
    #     for order in self:
    #         if order.pr_id:
    #             if order.approval_state != "approved":
    #                 raise UserError("RFQ must be approved before confirmation.")
    #
    #             if order.state != "vendor_accepted":
    #                 raise UserError("Vendor has not accepted the RFQ.")
    #
    #     return super().button_confirm()

    @api.model
    def create(self, vals):
        order = super().create(vals)
        if not order.pr_id:
            order.approval_state = "approved"
        return order

    def action_reject(self):
        for order in self:
            rules = order.approval_team_id.rule_ids.filtered(
                lambda r: r.min_amount <= order.amount_total <= r.max_amount
            )

            if not rules or self.env.user not in rules.approver_ids:
                raise UserError("You are not authorized to reject this RFQ.")

            self.env["purchase.approval.history"].sudo().create({
                "order_id": order.id,
                "user_id": self.env.user.id,
                "action": "rejected",
            })

            order.approval_state = "rejected"