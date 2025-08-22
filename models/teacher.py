# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError

class DssCustomersTeacher(models.Model):
    _name = 'dsscustomers.teacher'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'DSS Customers Teachers'
    _rec_name = 'teacher_name'

    # Thông tin chung
    teacher_name = fields.Char(string='Tên', required=True, tracking=True)
    birth_date = fields.Date(string='Ngày sinh', tracking=True, copy=False)
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác'),
    ],string='Giới tính', default='male', tracking=True)
    phonetc = fields.Char(string="Số điện thoại")
    email = fields.Char(string="Email")
    personal_mail = fields.Char(string="Email cá nhân")
    note = fields.Text(string='Mô tả') 
    active = fields.Boolean(string="Active", default=True)  
    session_ids = fields.One2many('dsscustomers.session', 'teacher_id', string="Lịch giảng dạy")
    session_count = fields.Integer(compute='_compute_session_details')
    attachmentcv_ids = fields.Many2many(comodel_name="ir.attachment",
                                                relation="m2m_ir_attachment_rel",
                                                column1="m2m_id",
                                                column2="attachment_id",
                                                string="CV")

    

    @api.model
    def create(self, vals):
        templates = super(DssCustomersTeacher,self).create(vals)
        # fix attachment ownership
        for template in templates:
            if template.attachmentcv_ids:
                template.attachmentcv_ids.write({'res_model': self._name, 'res_id': template.id})
        return templates

    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('teacher_name'):
            default['teacher_name'] = _("%s (Copy)", self.teacher_name)
        default['note'] = "Bản ghi đã sao chép"
        return super(DssCustomersTeacher, self).copy(default)

    @api.depends('session_ids')
    def _compute_session_details(self):
        for session in self:
            session.session_count = self.env['dsscustomers.session'].search_count(
                [('teacher_id', '=', self.id)])

    def count_sessions_details(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sessions',
            'view_mode': 'tree,form',
            'res_model': 'dsscustomers.session',
            'domain': [('teacher_id', '=', self.id)],
            'target': 'current',
        }




    
 