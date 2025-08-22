# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class ProcessingNghe(models.Model):
    _name = 'dsscustomers.processing.nghe'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'DSS Customers Processing Nghe'
    _rec_name = 'khachhangnghe_ids'

    # Ap dụng Visa 482/186/407/494
    khachhangnghe_ids = fields.Many2one('dsscustomers.dsscustomers', string="Khách hàng", required=True)
    masokh = fields.Char(related = 'khachhangnghe_ids.masokh')
    visa = fields.Selection(related = 'khachhangnghe_ids.visa',store=True)
    phonekh = fields.Char(related = 'khachhangnghe_ids.phonekh')
    thuthaphs = fields.Selection([('chuaduhs', 'Chưa đủ HS'),('daduhs', 'Đã đủ HS')],string="Thu thập hồ sơ gđ 1")
    hsphongvan = fields.Selection([('chuaduvpvhs', 'Chưa đủ HS'),('daduhspv', 'Đã đủ HS')],string="Hồ sơ phỏng vấn")
    pvvoichuld = fields.Selection([('doipv', 'Đợi PV'),('dapv', 'Đã PV'),('doikqpv', 'Đợi kết quả PV')],string="Phỏng vấn với chủ")
    sa = fields.Selection([('dangchuyenbi', 'Đang chuẩn bị'),('danop', 'Đã nộp'),('dathi', 'Đã thi')],string="SA")
    nomination = fields.Selection([('dangcbhsbaolanh', 'Đang chuẩn bị hồ sơ bảo lãnh'),('applied', 'Applied'),('approved', 'Approved')],string="Nomination")
    hsvisa = fields.Selection([('chuanbihs', 'Chuẩn bị HS'),('submitted', 'Submitted'),('granted', 'Granted'),('refused', 'Refused')],string="Hồ sơ Visa")
    ngaybay_granted = fields.Date(string="Ngày bay",tates={'draft': [('readonly', False)], 'sent': [('readonly', False)]},change_default=True)
    reapply_refused = fields.Char(string="Reapply",tates={'draft': [('readonly', False)], 'sent': [('readonly', False)]},change_default=True)
    lmia = fields.Selection([('applied_lmia', 'Applied'),('approved_lmia', 'Approved')],string="LMIA")
    userpro_id = fields.Many2one(related = 'khachhangnghe_ids.userpro_id',store=True)

    
 