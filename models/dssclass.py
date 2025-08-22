import calendar
from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class DssCustomersClassroom(models.Model):
    _name = 'dsscustomers.classroom'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'DSS Customers Class room'
    _rec_name = 'class_code'


    class_code = fields.Char(string="Mã lớp",size=32, required=True)
    flatform = fields.Selection([('online', 'Online'),
                                ('offline_cantho', 'Offline Cần Thơ' ),
                                ('offline_hn', 'Offline Hà Nội' ), 
                                ('offline_hcm', 'Offline HCM Hoàng Sa' ),       
                                ('offline_hcm', 'Offline HCM Q3' )],
                                string="Flatform",default=False)
    links_room = fields.Char(string="Link Zoom")
    ngaybatdau = fields.Date(string="Ngày bắt đầu học")
    ngaykethuc = fields.Date(string="Ngày kết thúc")
    ngaykethuctest = fields.Date(string="Ngày kết thúc Test")
    course_id = fields.Many2one('dsscustomers.course', string="Khóa học", required=True)
    monhoc_ids = fields.Many2many('dsscustomers.subject', string="Môn học")
    teacher_ids = fields.Many2many('dsscustomers.teacher', string="Giáo viên")
    days = fields.Char(string="Ngày")
    time = fields.Char(string="Thời gian")
    teacher_tags = fields.Char(string='Giáo viên', compute='_get_tags', store=True)
    dangky_ids = fields.One2many('dsscustomers.register', 'classroom_id', string="Đăng ký", copy=True)
    classstatus = fields.Selection([('ongoing', 'Đang diễn ra' ),
                                ('finished', 'Hoàn thành'),
                                ('plantoopen', 'Sắp tới')],
                                string="Trạng thái",default=False, compute='_compute_classstatus',readonly=True,store=True)
    note_class = fields.Text(string='Mô tả')
    students_count = fields.Integer(string='Số học viên', compute='_compute_students_count')
    userpic_id = fields.Many2one('res.users', 'Phụ trách', default=lambda self: self.env.user, track_visibility='onchange')
    links_cms = fields.Char(string="Link CMS")
    #Attendance
    attendancesheet_id = fields.One2many('dsscustomers.attendance.sheet', 'classroom_id', string="Điểm danh", copy=True)

    def _compute_students_count(self):
        for rec in self:
            students_count = self.env['dsscustomers.register'].search_count([('classroom_id', '=', rec.id)])
            rec.students_count = students_count


    @api.constrains('ngaybatdau','ngaykethuc')
    def _check_date_time(self):
        if self.ngaybatdau > self.ngaykethuc:
            raise ValidationError(_(
                'Không thể đặt Thời gian kết thúc trước Thời gian bắt đầu.'))
        
    @api.constrains('ngaybatdau','ngaykethuc')
    def _compute_classstatus(self):
        current_date = fields.Date.today()  # Get the current date
        for record in self:
            if record.ngaybatdau and record.ngaykethuc:
                if current_date < record.ngaybatdau:
                    # Before start date -> 'Not Started'
                    if record.classstatus != 'plantoopen':
                        record.write({'classstatus': 'plantoopen'})
                elif record.ngaybatdau <= current_date <= record.ngaykethuc:
                    # Between start date and end date -> 'Going'
                    if record.classstatus != 'ongoing':
                        record.write({'classstatus': 'ongoing'})
                elif current_date > record.ngaykethuc:
                    # After end date -> 'Finished'
                    if record.classstatus != 'finished':
                        record.write({'classstatus': 'finished'})

    def update_startus(self):
        records = self.search([]) 
        for record in records:          
            record._compute_classstatus()
        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }      
    @api.model
    def _status_classroom_scheduler_queue(self):

            current_date = fields.Date.today()  # Get the current date
            # Search all records (filter as necessary)
            records = self.search([])  # You can add a domain filter if needed
            for record in records:
                        if record.ngaybatdau and record.ngaykethuc:
                            if current_date < record.ngaybatdau:
                                # Before start date -> 'Not Started'
                                if record.classstatus != 'plantoopen':
                                    record.write({'classstatus': 'plantoopen'})
                            elif record.ngaybatdau <= current_date <= record.ngaykethuc:
                                # Between start date and end date -> 'Going'
                                if record.classstatus != 'ongoing':
                                    record.write({'classstatus': 'ongoing'})
                            elif current_date > record.ngaykethuc:
                                # After end date -> 'Finished'
                                if record.classstatus != 'finished':
                                    record.write({'classstatus': 'finished'})

    @api.model
    @api.depends('teacher_ids')
    def _get_tags(self):
        for rec in self:
            if rec.teacher_ids:
                teacher_tags = ', '.join([p.teacher_name for p in rec.teacher_ids])
            else:
                teacher_tags = ''
            rec.teacher_tags = teacher_tags


    def action_dsscustomers_attendance_sheet(self):
        # Tạo một bản ghi mới cho bảng điểm danh
        attendance_sheet = self.env['dsscustomers.attendance.sheet'].create({
            'classroom_id': self.id,
            'attendance_date': fields.Date.today(),
            'state': 'draft'
        })

        # Lấy danh sách học viên đã đăng ký vào lớp
        student_ids = self.dangky_ids.mapped('sinhvien_ids')

        # Tạo danh sách học viên cho bảng điểm danh
        attendance_lines = [(0, 0, {
            'attendance_id': attendance_sheet.id,
            'student_id': student.id,
            'present': True,  # Mặc định vắng mặt, giáo viên sẽ cập nhật sau
        }) for student in student_ids if student]

        if attendance_lines:
            attendance_sheet.write({'attendance_line': attendance_lines})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Attendance Sheet',
            'res_model': 'dsscustomers.attendance.sheet',
            'res_id': attendance_sheet.id,
            'view_mode': 'form',
            'target': 'current'
        }