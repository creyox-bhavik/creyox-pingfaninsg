# -*- coding: utf-8 -*-
from odoo import models, fields


class PaymentInfo(models.Model):
    _name = 'payment.info'
    _description = 'Account Payment Info'

    payment_id = fields.Many2one('account.payment')
    invoice_name = fields.Char()
    payment_amount = fields.Float()
