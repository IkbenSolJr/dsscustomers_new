from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class DssCustomersRegister(models.Model):
    _name = 'dsscustomers.register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'DSS Customers Class Register'
    _rec_name = 'sinhvien_ids'


    # Thông tin chung
    madangky = fields.Char(
        'Số đăng ký', copy=False,
        required=True, readonly=True, store=True,
        default=lambda self:
        self.env['ir.sequence'].next_by_code('dsscustomers.register'))
    sinhvien_ids = fields.Many2one('dsscustomers.dsscustomers', string="Học viên", required=True)
    masokh = fields.Char(related = 'sinhvien_ids.masokh', store=True )    
    visa = fields.Selection(related = 'sinhvien_ids.visa', store=True)
    phonekh = fields.Char(related = 'sinhvien_ids.phonekh', store=True )
    classroom_id = fields.Many2one('dsscustomers.classroom', string="Lớp học",copy=True)
    note = fields.Text(string="Teacher's feedback")
    course_id = fields.Many2one(related = 'classroom_id.course_id',store=True)
    # teacher_id = fields.Many2one(related = 'classroom_id.teacher_id',store=True)
    classstatus = fields.Selection(related = 'classroom_id.classstatus', store=True)
    links_room = fields.Char(related = 'classroom_id.links_room',store=True)
    ngaybatdau = fields.Date(related = 'classroom_id.ngaybatdau',store=True)
    ngaykethuc = fields.Date(related = 'classroom_id.ngaykethuc',store=True)
    actual_start =  fields.Date(string="Bắt đầu thực tế",default=lambda self: fields.Datetime.now())
    actual_end =  fields.Date(string="Kết thúc thực tế")
    feedback_training = fields.Text(string="Tình trạng ĐTTA")
    #Bổ sung
    flatform = fields.Selection(related = 'classroom_id.flatform')
    userpic_id = fields.Many2one(related = 'classroom_id.userpic_id')
    students_count = fields.Integer(related = 'classroom_id.students_count')
    ge_score = fields.Float(string="Điểm thi GE") 
    ielts_list = fields.Float(string="IELTS Listening Score")
    ielts_writ = fields.Float(string="IELTS Writing Score")
    ielts_speak = fields.Float(string="IELTS Speaking Score")
    ielts_over = fields.Float(string="IELTS Overall")
    teacher_ids = fields.Many2many(related = 'classroom_id.teacher_ids')
    days = fields.Char(related = 'classroom_id.days')
    time = fields.Char(related = 'classroom_id.time')
    attendance_line_ids = fields.One2many('dsscustomers.attendance.line','student_id',string="Điểm danh")
    course_id = fields.Many2one('dsscustomers.course', string="Khóa học", required=True)
    monhoc_ids = fields.Many2many('dsscustomers.subject', string="Môn học")
    
    # Bổ sung
    interview = fields.Text(string="INTERVIEW")
    communication = fields.Text(string="COMMUNICATION")
    tongtiendo = fields.Text(string="Tổng tiến độ")
    tylehoanthanh = fields.Selection([   
    ('25', '25'), 
    ('50', '50'),
    ('75', '75'),
    ('100', '100'),    
    ],string="Mức độ hoàn thành", default=False)

    # Chung    
    # teamphutrach = fields.Many2one('hr.department', string="Team", default=lambda self: self.env.user.department_id, track_visibility='onchange')
    # user_id = fields.Many2one('res.users', 'Sale', default=lambda self: self.env.user, track_visibility='onchange')
    # usercs_id = fields.Many2one('res.users', 'Phụ trách CS', default=lambda self: self.env.user, track_visibility='onchange')
    # userpro_id = fields.Many2one('res.users', 'Phụ trách Processing', default=lambda self: self.env.user, track_visibility='onchange')
    # userdt_id = fields.Many2one('res.users', 'Phụ trách Đào tạo', default=lambda self: self.env.user, track_visibility='onchange')
    

    def action_dsscustomers_attendance_line(self):        
            return {
                'type': 'ir.actions.act_window',
                'name': 'Attendance Line',
                'res_model': 'dsscustomers.attendance.line',
                'domain': [('student_id', '=', self.id)],
                'context': {'default_student_id': self.id},
                'view_mode': 'tree,form',
                'target': 'current',
            }

    



    # def get_allocation(self):
    #     action = self.env.ref('dsscustomers.'
    #                           'act_open_dsscustomers_assignment_view').read()[0]
    #     action['domain'] = [('allocation_ids', 'in', self.ids)]
    #     return action

    # def compute_count_assignment(self):
    #     for record in self:
    #         record.assignment_count = self.env['op.assignment'].search_count(
    #             [('allocation_ids', '=', self.id)])


    
    @api.model
    def create_training_channel(self):
        """Tạo hoặc lấy nhóm Nhóm Đào tạo"""
        channel = self.env['mail.channel'].sudo().search([('name', '=', 'Đào tạo')], limit=1)
        if not channel:
            channel = self.env['mail.channel'].sudo().create({
                    'name': 'Đào tạo',
                    'channel_type': 'channel',  # 'channel' = public channel
                    'public': 'public',  # Công khai để tất cả nhân viên có thể tham gia
            })
        return channel

    @api.model
    def send_message_to_training_channel(self):
        """Gửi thông báo vào nhóm Nhóm Đào tạo"""
        channel = self.create_training_channel()

        if channel:
            for record in self:
                if not record.sinhvien_ids:
                    continue  # Bỏ qua nếu không có khách hàng

                base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
                customer_url = f"{base_url}/web#id={record.id}&model=dsscustomers.dsscustomers&view_type=form"

                message = f"""
                    <b>Cập nhật đào tạo!</b><br/>
                    Khách hàng: <a href="{customer_url}" target="_blank">{record.sinhvien_ids.khachhang_id.name}</a><br/>
                    Cập nhật: {record.tongtiendo or 'Không có dữ liệu'}
                """

                channel.message_post(
                    body=message,
                    message_type="comment",
                    subtype_xmlid="mail.mt_comment"
                )

    @api.model
    def create(self, vals):
        """Gửi thông báo khi tạo mới"""
        record = super(DssCustomersRegister, self).create(vals)
        record.send_message_to_training_channel()
        return record

    def write(self, vals):
        """Gửi thông báo khi có thay đổi"""
        res = super(DssCustomersRegister, self).write(vals)
        self.send_message_to_training_channel()
        return res