import calendar
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
import pytz

week_days = [(calendar.day_name[0], _(calendar.day_name[0])),
             (calendar.day_name[1], _(calendar.day_name[1])),
             (calendar.day_name[2], _(calendar.day_name[2])),
             (calendar.day_name[3], _(calendar.day_name[3])),
             (calendar.day_name[4], _(calendar.day_name[4])),
             (calendar.day_name[5], _(calendar.day_name[5])),
             (calendar.day_name[6], _(calendar.day_name[6]))]


class ClassSession(models.Model):
    _name = "dsscustomers.session"
    _inherit = ["mail.thread"]
    _description = "Dss Customers Sessions"

    name = fields.Char(compute='_compute_name', string='Tên', store=True)
    timing_id = fields.Many2one(
        'dsscustomers.timing', 'Thời gian', tracking=True)
    start_datetime = fields.Datetime(
        'Bắt đầu', required=True,
        default=lambda self: fields.Datetime.now())
    end_datetime = fields.Datetime(
        'kết thúc', required=True)
    course_id = fields.Many2one(
        'dsscustomers.course', 'Khóa học', required=True)
    monhoc_ids = fields.Many2many('dsscustomers.subject', string="Môn học")
    teacher_id = fields.Many2one(
        'dsscustomers.teacher', 'Giáo viên')
    classroom_id = fields.Many2one(
        'dsscustomers.classroom', 'Lớp học')
    color = fields.Integer('Màu sắc')
    type = fields.Char(compute='_compute_day', string='Ngày', store=True)
    state = fields.Selection(
        [('draft', 'Dự thảo'), ('confirm', 'Đã xác nhận'),
         ('done', 'Hoàn thành'), ('cancel', 'Hủy')],
        string='Trạng thái', default='draft')
    active = fields.Boolean(default=True)
    days = fields.Selection([
        ('monday', 'Thứ 2'),
        ('tuesday', 'Thứ 3'),
        ('wednesday', 'Thứ 4'),
        ('thursday', 'Thứ 5'),
        ('friday', 'Thứ 6'),
        ('saturday', 'Thứ 7'),
        ('sunday', 'Chủ nhật')],
        'Các ngày',
        group_expand='_expand_groups', store=True
    )
    timing = fields.Char(compute='_compute_timing')

    @api.depends('start_datetime', 'end_datetime')
    def _compute_timing(self):
        tz = pytz.timezone(self.env.user.tz)
        for session in self:
            session.timing = str(session.start_datetime.astimezone(tz).strftime('%I:%M%p')) + ' - ' + str(
                session.end_datetime.astimezone(tz).strftime('%I:%M%p'))

    @api.model
    def _expand_groups(self, days, domain, order):
        weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        return [day for day in weekdays if day in days]

    @api.depends('start_datetime')
    def _compute_day(self):
        for record in self:
            record.type = fields.Datetime.from_string(
                record.start_datetime).strftime("%A")
            record.days = fields.Datetime.from_string(
                record.start_datetime).strftime("%A").lower()

    @api.depends('teacher_id', 'start_datetime')
    def _compute_name(self):
        tz = pytz.timezone(self.env.user.tz)
        for session in self:
            if session.teacher_id \
                    and session.start_datetime and session.end_datetime:
                session.name = \
                    session.teacher_id.teacher_name + ': ' + str(
                        session.start_datetime.astimezone(tz).strftime('%I:%M%p')) + ' - ' + str(
                        session.end_datetime.astimezone(tz).strftime('%I:%M%p'))


    def lecture_draft(self):
        self.state = 'draft'

    def lecture_confirm(self):
        self.state = 'confirm'

    def lecture_done(self):
        self.state = 'done'

    def lecture_cancel(self):
        self.state = 'cancel'

    @api.constrains('start_datetime', 'end_datetime')
    def _check_date_time(self):
        if self.start_datetime > self.end_datetime:
            raise ValidationError(_(
                'End Time cannot be set before Start Time.'))
        
        
    def write(self, vals):
        data = super(ClassSession,
                     self.with_context(check_move_validity=False)).write(vals)
        for session in self:
            if session.state not in ('draft', 'done'):
                session.notify_user()
        return data

    def notify_user(self):
        for session in self:
            template = self.env.ref(
                'openeducat_timetable.session_details_changes',
                raise_if_not_found=False)
            template.send_mail(session.id)



    @api.model
    def get_import_templates(self):
        return [{
            'label': _('Import Template for Sessions'),
            'template': '/dsscustomers/static/xls/op_session.xls'
        }]

    
class DsscustomersTiming(models.Model):
    _name = "dsscustomers.timing"
    _description = "Period"
    _order = "sequence"

    name = fields.Char('Name', size=16, required=True)
    hour = fields.Selection(
        [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'),
         ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'),
         ('11', '11'), ('12', '12')], 'Hours', required=True)
    minute = fields.Selection(
        [('00', '00'), ('15', '15'), ('30', '30'), ('45', '45')], 'Minute',
        required=True)
    duration = fields.Float('Duration')
    am_pm = fields.Selection(
        [('am', 'AM'), ('pm', 'PM')], 'AM/PM', required=True)
    sequence = fields.Integer('Sequence')