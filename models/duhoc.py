# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP

class ProcessingDuhoc(models.Model):
    _name = 'dsscustomers.processing.duhoc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'DSS Customers Processing Study'
    _rec_name = 'khachhangdh_ids'

    sottpro = fields.Char(string='Stt', required=True, copy=False, readonly=True,default=lambda self: _('New'))
    masokh = fields.Char(related = 'khachhangdh_ids.masokh')    
    khachhangdh_ids = fields.Many2one('dsscustomers.dsscustomers', string="Khách hàng",required=True)
    visa = fields.Selection(related = 'khachhangdh_ids.visa',store=True)
    phonekh = fields.Char(related = 'khachhangdh_ids.phonekh')
    guichecklist = fields.Boolean(string="Gửi Checklist", default=False)
    nhaphskh= fields.Text(string="Nhận hồ sơ từ khách")
    dichhskh = fields.Boolean(string="Dịch thuật hồ sơ", default=False)
    # bangta = fields.Selection([('ielts', 'IELTS'),('pte', 'PTE')],string="Bằng tiếng Anh",default=False)
    # sodiemta = fields.Float(string="Số điểm")
    xinoffer= fields.Text(string="Xin offer")
    nhanoffer = fields.Selection([('conditionaloffer', 'Conditional Offer'),('unconditionaloffer', 'Unconditional Offer')],
    string="Nhận Offer",default=False)
    tennganhhoc= fields.Text(string="Tên ngành học")
    ngaynhaphoc = fields.Date(string="Ngày nhập học")
    donghocphioshc = fields.Boolean(string="Đóng học phí/OSHC", default=False)
    coes = fields.Boolean(string="COEs", default=False)
    vietsopgte = fields.Boolean(string="Viết SOP/GTE", default=False)
    dienformvisa = fields.Boolean(string="Điền form Visa", default=False)
    nopvisa = fields.Boolean(string="Nộp Visa", default=False)
    bennopvisa= fields.Text(string="Bên nộp Visa")
    ngaynopvisa = fields.Date(string="Ngày nộp Visa")
    tappv = fields.Selection([('dangtappv', 'Đang tập'),('datappv', 'Đã tập xong')],string="Tập phỏng vấn",default=False)
    nhankqpv = fields.Selection([('grant', 'Grant'),('refuse', 'Refuse')],string="Nhận kết quả",default=False)
    huongdanbay = fields.Boolean(string="Hướng dẫn bay", default=False)   
    ngayhethanvisa = fields.Date(string="Ngày hết hạn Visa")
    processinginfo_ids = fields.One2many('dsscustomers.processing.curency', 'khcurency_ids',string="Thông tin Processing")
    total = fields.Float(string="Tổng", compute="_compute_total")
    userpro_id = fields.Many2one(related = 'khachhangdh_ids.userpro_id',store=True)


    @api.model
    def create(self, vals):
        if vals.get('sottpro', _('New')) == _('New'):
           vals['sottpro'] = self.env['ir.sequence'].next_by_code('dsscustomers.processing.duhoc') or _('New')
        res = super(ProcessingDuhoc, self).create(vals)
        return res

    @api.depends('processinginfo_ids.sotien')
    def _compute_total(self):
        for record in self:
            record.total = sum(record.processinginfo_ids.mapped('sotien'))

    # def create(self, vals, context=None):
    #         if vals.get('khachhangdh_ids'):
    #             count = len(vals.get('khachhangdh_ids'))
    #         if count > 1:
    #             raise (_('Warning!'), _('Limit to create 3 Lines'))
    #         return super(ProcessingDuhoc, self).create(vals)        

     