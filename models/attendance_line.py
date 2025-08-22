# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError



class DssCustomersClassroom(models.Model):
    _name = 'dsscustomers.attendance.line'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'DSS Customers Attendance lines'
    _rec_name = "student_id"


    student_id = fields.Many2one('dsscustomers.register', string="Học viên", tracking=True)
    attendance_type_id = fields.Many2one('dsscustomers.attendance.type', 'Kiểu điểm danh', required=False, tracking=True, copy=True)
    present = fields.Boolean('Có mặt', default=True, tracking=True)
    excused = fields.Boolean('Vắng mặt có lý do', tracking=True)
    absent = fields.Boolean('Vắng mặt Không có lý do', tracking=True)
    late = fields.Boolean('Muộn', tracking=True)
    remark = fields.Char('Nhận xét', size=256, tracking=True)   
    active = fields.Boolean(default=True)
    attendance_id = fields.Many2one('dsscustomers.attendance.sheet', string="Bảng điểm danh",required=True, tracking=True, ondelete="cascade")
    classroom_id = fields.Many2one(related='attendance_id.classroom_id', store=True)
    course_id = fields.Many2one(related='attendance_id.course_id', store=True)  
    register_id = fields.Char(related='attendance_id.register_id', store=True)
    attendance_date = fields.Date(related='attendance_id.attendance_date', store=True, readonly=True, tracking=True)
    subject_ids = fields.Many2many('dsscustomers.subject', string='Các Môn học')


    _sql_constraints = [
        ('unique_student',
         'unique(student_id,attendance_id,attendance_date)',
         'Student must be unique per Attendance.')
    ]

    @api.onchange('attendance_type_id')
    def onchange_attendance_type(self):
        if self.attendance_type_id:
            self.present = self.attendance_type_id.present
            self.excused = self.attendance_type_id.excused
            self.absent = self.attendance_type_id.absent
            self.late = self.attendance_type_id.late

    @api.onchange('present')
    def onchange_present(self):
        if self.present:
            self.late = False
            self.excused = False
            self.absent = False

    @api.onchange('absent')
    def onchange_absent(self):
        if self.absent:
            self.present = False
            self.late = False
            self.excused = False

    @api.onchange('excused')
    def onchange_excused(self):
        if self.excused:
            self.present = False
            self.late = False
            self.absent = False

    @api.onchange('late')
    def onchange_late(self):
        if self.late:
            self.present = False
            self.excused = False
            self.absent = False


class DssCustomersAttendanceType(models.Model):
    _name = "dsscustomers.attendance.type"
    _inherit = ["mail.thread"]
    _description = "Attendance Type"

    name = fields.Char(
        'Tên', size=20, required=True, tracking=True)
    active = fields.Boolean(default=True)
    present = fields.Boolean(
        'Có mặt ?', tracking=True)
    excused = fields.Boolean(
        'Đã báo ?', tracking=True)
    absent = fields.Boolean('Vắng mặt', tracking=True)
    late = fields.Boolean('Muộn', tracking=True)
