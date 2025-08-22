# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP


class ProcessingCurency(models.Model):
    _name = 'dsscustomers.processing.curency'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'DSS Customers Processing Curency'
    _rec_name = 'khcurency_ids'

    khcurency_ids = fields.Many2one('dsscustomers.processing.duhoc', string="Khách hàng",required=True)
    masokh = fields.Char(related = 'khcurency_ids.masokh')
    visa = fields.Selection(related = 'khcurency_ids.visa')
    phonekh = fields.Char(related = 'khcurency_ids.phonekh')
    lanthu = fields.Selection([
    ('ttcomdotmot', 'Com đợt 1'),
    ('ttcomdothai', 'Com đợt 2'),
    ('ttcomdotba', 'Com đợt 3'),
    ('ttcomdotbon', 'Com đợt 4'),
    ('ttcomdotnam', 'Com đợt 5'),
    ('ttcomdotsau', 'Com đợt 6'),
    ('ttcomdotbay', 'Com đợt 7'),
    ('ttcomdottam', 'Com đợt 8'),
    ('ttcomdotchin', 'Com đợt 9'),
    ('ttcomdotmuoi', 'Com đợt 10'),
    ('ttcomdotmmot', 'Com đợt 11'),
    ('ttcomdotmhai', 'Com đợt 12')],
    string="Thanh toán", default=False)

    ngaycom = fields.Date(string="Ngày")
    sotien = fields.Monetary(string="Số tiền",currency_field='currency_ids')
    currency_ids = fields.Many2one('res.currency', string="Đơn vị tiền", store=True, readonly=False)    
