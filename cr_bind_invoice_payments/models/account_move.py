# -*- coding: utf-8 -*-
from odoo import models, fields,api
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
            
            for rec in self:
                rec.payment_id.name = rec.payment_id.old_name
            return res

        else:
            res = super().write(vals)
            return res
    

    
    def _inverse_name(self):
        self._conditional_add_to_compute('payment_reference', lambda move: (
            move.name and move.name != '/'
        ))

        _logger.info("\n\n 54 %s",self)        
    

    @api.depends('posted_before', 'state', 'journal_id', 'date')
    def _compute_name(self):
        self = self.sorted(lambda m: (m.date, m.ref or '', m.id))

        for move in self:
            move_has_name = move.name and move.name != '/'
            if move_has_name or move.state != 'posted':
                if not move.posted_before and not move._sequence_matches_date():
                    if move._get_last_sequence(lock=False):
                        # The name does not match the date and the move is not the first in the period:
                        # Reset to draft
                        move.name = False
                        continue
                else:
                    if move_has_name and move.posted_before or not move_has_name and move._get_last_sequence(lock=False):
                        # The move either
                        # - has a name and was posted before, or
                        # - doesn't have a name, but is not the first in the period
                        # so we don't recompute the name
                        continue
            if move.date and (not move_has_name or not move._sequence_matches_date()):
                move._set_next_sequence()

        self.filtered(lambda m: not m.name and not move.quick_edit_mode).name = '/'
        self._inverse_name()

        _logger.info("\n\n 83 %s",self)        