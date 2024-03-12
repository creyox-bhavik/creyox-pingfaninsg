# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    old_name = fields.Char()
    cr_payment_reference = fields.Char()
    payment_info_line = fields.One2many('payment.info', 'payment_id',copy=True)

    @api.model
    def create(self, values):
        res = super().create(values)
        res.sudo().name = '/'
        res.sudo().move_id._compute_name()
        return res

    # def _synchronize_to_moves(self, changed_fields):
    #     _logger.info("\n\n 22")        
    

    def write(self,vals):
        _logger.info("\n\n 26 %s", vals)        
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