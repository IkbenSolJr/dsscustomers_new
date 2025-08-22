import calendar
from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class DssCustomersClassroomwork(models.Model):
    _name = 'dsscustomers.classroomwork'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'DSS Customers Class work room '
    _rec_name = 'class_code'

    class_code = fields.Char(string="Mã lớp",size=32, required=True)
    flatform = fields.Selection([('online', 'Online'),
                                ('offline_cantho', 'Offline Cần Thơ' ),
                                ('offline_hn', 'Offline Hà Nội' ), 
                                ('offline_hcm', 'Offline HCM Hoàng Sa' ),       
                                ('offline_hcm', 'Offline HCM Q3' )],
                                string="Flatform",default=False)
    links_room = fields.Char(string="Link Zoom")
    ngaybatdau = fields.Date(string="Ngày bắt đầu")
    ngaykethuc = fields.Date(string="Ngày kết thúc")
    duration = fields.Float('Thời lượng', store=True, readonly=False)
    ngaykethuctest = fields.Date(string="Ngày kết thúc Test")
    coursework_id = fields.Many2one('dsscustomers.coursework', string="Khóa học", required=True)
    teacher_ids = fields.Many2many('dsscustomers.teacherwork', string="Giáo viên")
    teacher_tags = fields.Char(string='Giáo viên', compute='_get_teacher_tags', store=True)
    days = fields.Char(string="Ngày")
    time = fields.Char(string="Thời gian")    
    dangkynghe_ids = fields.One2many('dsscustomers.registerwork', 'classroomwork_id', string="Đăng ký", copy=True)
    classstatus = fields.Selection([('ongoing', 'Đang diễn ra' ),
                                ('finished', 'Hoàn thành'),
                                ('plantoopen', 'Dự kiến')],
                                string="Trạng thái",default=False, compute='_compute_classworkstatus',store=True,readonly=True)
    note_class = fields.Text(string='Ghi chú')
    students_count = fields.Integer(string='Tổng Số học viên', compute='_compute_students_count')
    userpic_id = fields.Many2one('res.users', 'Phụ trách', default=lambda self: self.env.user, track_visibility='onchange')
    links_cms = fields.Char(string="Link CMS")


    def _compute_students_count(self):
        for rec in self:
            students_count = self.env['dsscustomers.registerwork'].search_count([('classroomwork_id', '=', rec.id)])
            rec.students_count = students_count


    @api.constrains('ngaybatdau','ngaykethuc')
    def _check_date_time(self):
        if self.ngaybatdau > self.ngaykethuc:
            raise ValidationError(_('Ngày kết thúc phải lớn hơn ngày bắt đầu.'))
        
    @api.constrains('ngaybatdau','ngaykethuc')
    def _compute_classworkstatus(self):
            today = fields.Date.today()
            self.classstatus = 'plantoopen'
            for rec in self:
                if rec.ngaybatdau and rec.ngaybatdau <= today:
                    rec.classstatus = 'ongoing' 
                if rec.ngaykethuc and rec.ngaykethuc < today:
                    rec.classstatus = 'finished' 

    @api.model
    @api.depends('teacher_ids')
    def _get_teacher_tags(self):
        for rec in self:
            if rec.teacher_ids:
                teacher_tags = ', '.join([p.teacherwork_name for p in rec.teacher_ids])
            else:
                teacher_tags = ''
            rec.teacher_tags = teacher_tags