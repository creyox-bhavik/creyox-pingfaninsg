# -*- coding: utf-8 -*-
from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

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

    def write(self,vals):
        _logger.info("\n\n 17 %s",vals)        

        if 'name' in vals:

            _logger.info("\n\n 36 %s",vals)        
            del vals['name']
            _logger.info("\n\n 38 %s",vals)        
            res = super().write(vals)

            return res

        else:
            res = super().write(vals)
            return res