# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    old_name = fields.Char()
    cr_payment_reference = fields.Char()

    @api.model
    def create(self, values):
        res = super().create(values)
        res.sudo().name = '/'
        res.sudo().move_id._compute_name()
        return res
