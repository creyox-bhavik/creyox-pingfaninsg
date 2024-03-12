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

    def _synchronize_to_moves(self, changed_fields):
        _logger.info("\n\n 22" + 22)        
    

    def write(self,vals):
        _logger.info("\n\n 26" + vals)        
        res = super().write(vals)

        return res
