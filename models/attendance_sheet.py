from odoo import models, fields, api, _


class DssCustomersAttendanceSheet(models.Model):
    _name = "dsscustomers.attendance.sheet"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'DSS Customers Attendance Sheet'
    _order = "attendance_date desc"


    name = fields.Char('Tên', readonly=True, size=32)
    register_id = fields.Char(string="Đăng ký điểm danh", tracking=True)
    classroom_id = fields.Many2one('dsscustomers.classroom', 'Lớp học', store=True)
    course_id = fields.Many2one(related = 'classroom_id.course_id',store=True)
    subject_ids = fields.Many2many('dsscustomers.subject', string='Các Môn học')
    
    
    session_id = fields.Many2one('dsscustomers.session', 'Lịch giảng dạy')
    attendance_date = fields.Date('Ngày', required=True, default=lambda self: fields.Date.today(), tracking=True)
    active = fields.Boolean(default=True)
    state = fields.Selection(
        [('draft', 'Dự thảo'), ('start', 'Bắt đầu điểm danh'),
         ('done', 'Đã điểm danh'), ('cancel', 'Hủy')],
        'Tình trạng', default='draft', tracking=True)
    attendance_line = fields.One2many('dsscustomers.attendance.line', 'attendance_id', string="Chi tiết điểm danh", copy=True)
    # dangky_ids = fields.Many2many('dsscustomers.register', string='Thêm học viên')

    def attendance_draft(self):
        self.state = 'draft'

    def attendance_start(self):
        self.state = 'start'

    def attendance_done(self):
        self.state = 'done'

    def attendance_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        sheet_sequence = self.env['ir.sequence'].next_by_code('dsscustomers.attendance.sheet') or 'New'
        register = str(vals.get('register_id', 'NoRegister'))
        vals['name'] = register + sheet_sequence
        return super(DssCustomersAttendanceSheet, self).create(vals)

    @api.onchange('register_id')
    def _onchange_register_id(self):
        """Cập nhật tên điểm danh khi sửa register_id"""
        if self.register_id:
            sheet_sequence = self.env['ir.sequence'].next_by_code('dsscustomers.attendance.sheet') or 'New'
            self.name = f"{self.register_id}{sheet_sequence}"

    def write(self, vals):
        """Cập nhật tên điểm danh khi sửa register_id"""
        if 'register_id' in vals:
            sheet_sequence = self.env['ir.sequence'].next_by_code('dsscustomers.attendance.sheet') or 'New'
            vals['name'] = f"{vals.get('register_id', self.register_id)}{sheet_sequence}"
        return super(DssCustomersAttendanceSheet, self).write(vals)