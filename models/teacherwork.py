# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class DssCustomersTeacherwork(models.Model):
    _name = 'dsscustomers.teacherwork'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'DSS Customers Teachers'
    _rec_name = 'teacherwork_name'

    # Thông tin chung
    teacherwork_name = fields.Char(string='Họ và tên', required=True, tracking=True)
    birth_date = fields.Date(string='Ngày sinh', tracking=True, copy=False)
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
    ], default='male', tracking=True)
    phonetc = fields.Char(string="Điện thoại")
    email = fields.Char(string="Email")
    personal_mail = fields.Char(string="Email khác")
    note = fields.Text(string='Ghi chú') 

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('teacherwork_name'):
            default['teacherwork_name'] = _("%s (Copy)", self.teacherwork_name)
        default['note'] = "Copied Record"
        return super(DssCustomersTeacherwork, self).copy(default)

  



    
 