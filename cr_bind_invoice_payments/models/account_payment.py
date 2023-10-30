# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    old_name = fields.Char()
    cr_payment_reference = fields.Char()
