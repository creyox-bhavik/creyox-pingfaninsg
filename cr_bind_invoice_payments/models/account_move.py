# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountMove(models.Model):
    _inherit = 'account.move'

    old_name = fields.Char()

    def _get_starting_sequence(self):
        # EXTENDS account sequence.mixin
        self.ensure_one()
        is_payment = self.payment_id or self._context.get('is_payment')
        if self.journal_id.type == 'sale':
            starting_sequence = "%s/%04d/00000" % (
                self.journal_id.code, self.date.year)
        elif self.journal_id.type in ['bank', 'cash']:
            starting_sequence = "%s%04d%02d-0000" % (
                self.journal_id.code, self.date.year, self.date.month)
        else:
            starting_sequence = "%s/%04d/%02d/0000" % (
                self.journal_id.code, self.date.year, self.date.month)
        if self.journal_id.refund_sequence and self.move_type in ('out_refund', 'in_refund'):
            starting_sequence = "R" + starting_sequence
        # if self.journal_id.payment_sequence and is_payment:
        #     starting_sequence = "P" + starting_sequence
        return starting_sequence
    
    def _auto_init(self):
        pass