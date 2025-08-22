from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class DssCustomersRegisterWork(models.Model):
    _name = 'dsscustomers.registerwork'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'DSS Customers Class Register Work'
    _rec_name = 'sinhvien_ids'


    # Thông tin chung
    madangkynghe = fields.Char(
        'Mã Đăng ký', copy=False,
        required=True, readonly=True, store=True,
        default=lambda self:
        self.env['ir.sequence'].next_by_code('dsscustomers.registerwork'))
    sinhvien_ids = fields.Many2one('dsscustomers.dsscustomers', string="Học viên", required=True)
    masokh = fields.Char(related = 'sinhvien_ids.masokh')    
    visa = fields.Selection(related = 'sinhvien_ids.visa', store=True)
    phonekh = fields.Char(related = 'sinhvien_ids.phonekh')
    classroomwork_id = fields.Many2one('dsscustomers.classroomwork', string="Lớp học",copy=True)
    note = fields.Text(string='Ghi chú')
    coursework_id = fields.Many2one(related = 'classroomwork_id.coursework_id',store=True)
    # teacherwork_id = fields.Many2one(related = 'classroomwork_id.teacherwork_id',store=True)
    classstatus = fields.Selection(related = 'classroomwork_id.classstatus',store=True)
    links_room = fields.Char(related = 'classroomwork_id.links_room',store=True)
    score = fields.Float(string="Điểm")  
    ngaybatdau = fields.Date(related = 'classroomwork_id.ngaybatdau',store=True)
    ngaykethuc = fields.Date(related = 'classroomwork_id.ngaykethuc',store=True)
    feedback_training = fields.Text(string="Tình trạng ĐT Nghề")
    flatform = fields.Selection(related = 'classroomwork_id.flatform')
    userpic_id = fields.Many2one(related = 'classroomwork_id.userpic_id')
    students_count = fields.Integer(related = 'classroomwork_id.students_count')
    # Điểm
    vs_score = fields.Float(string="Vệ sinh/Hygiene(10)")
    chuanbi_sc = fields.Float(string="Sự chuẩn bị/Preparation (35)")
    trinhbay_sc = fields.Float(string="Trình bày sản phẩm/Presentation (20)")
    kynang_sc = fields.Float(string="Kỹ năng, thao tác sử dụng dao/Skill, technique(35)")
    tongdiem = fields.Float(string="Tổng/Total")

    # Bổ sung

    lythuyet = fields.Text(string='Lý thuyết')
    thuchanh = fields.Text(string='Thực hành')
    thuctap = fields.Text(string='Thực tập')
    tongtiendo = fields.Text(string='Tổng tiên độ')
    tylehoanthanhnghe = fields.Selection([   
        ('25', '25'), 
        ('50', '50'),
        ('75', '75'),
        ('100', '100'),    
        ],string="Hoàn thành nghề", default=False)

 