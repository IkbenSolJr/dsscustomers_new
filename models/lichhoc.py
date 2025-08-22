# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class DsscustomersLichhoc(models.Model):
    _name = 'dsscustomers.lichhoc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherit = 'dsscustomers.dsscustomers'
    _description = 'Lịch học'
    _rec_name = 'khachhang_ids'


    sott = fields.Char(string='Stt', required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))
    date_lichhoc= fields.Date(string="Ngày")
    khachhang_ids = fields.Many2one('dsscustomers.dsscustomers', string="Khách hàng", required=True)
    thanhphodt  = fields.Char(string="Tỉnh/Thành phố")
    ngayhoc = fields.Selection([('thuhai', 'Thứ 2'),
                                  ('thuba', 'Thứ 3'),
                                  ('thutu', 'Thứ 4'),
                                  ('thunam', 'Thứ 5'),
                                  ('thusau', 'Thứ 6'),
                                  ('thubay', 'Thứ 7'),
                                  ('cn', 'Chủ nhật')],
                                 string="Thứ")
    giohoc = fields.Char(string="Giờ")
    masokh = fields.Char(string="MSKH")
    giaovien = fields.Many2one('hr.employee', string="Giáo viên", default=lambda self: self.env.user.employee_id, required=True)


    @api.model
    def create(self, vals):
        if vals.get('sott', _('New')) == _('New'):
           vals['sott'] = self.env['ir.sequence'].next_by_code('dsscustomers.lichhoc') or _('New')
        res = super(DsscustomersLichhoc, self).create(vals)
        return res
