import calendar
from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError


class DssCustomersClassroom(models.Model):
    _name = 'dsscustomers.lichhocnghe'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Lịch học nghề'
    # _rec_name = 'class_code'


    from_date = fields.Date("From Date")
    to_date = fields.Date("To Date")
    month_days = fields.Selection([('monday','Thứ 2'),('tuesday','Thứ 3'),
                                ('wednesday','Thứ 4'),('thursday','Thứ 5'),
                                ('friday','Thứ 6'),('saturday','Thứ 7'),
                                ('sunday','Chủ nhật')], "Ngày")
    day_count = fields.Integer("Số ngày")



    def _compute_students_count(self):
        for rec in self:
            students_count = self.env['dsscustomers.registerwork'].search_count([('classroomwork_id', '=', rec.id)])
            rec.students_count = students_count


    @api.constrains('ngaybatdau','ngaykethuc')
    def _check_date_time(self):
        if self.ngaybatdau > self.ngaykethuc:
            raise ValidationError(_(
                'End Time cannot be set before Start Time.'))        

    
 