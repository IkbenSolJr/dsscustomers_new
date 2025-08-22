# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP



class DssSubject(models.Model):
    _name = "dsscustomers.subject"
    _inherit = "mail.thread"
    _description = "Môn học"

    name = fields.Char('Tên môn học', size=128, required=True)
    code = fields.Char('Mã môn', size=256, required=True)
    grade_weightage = fields.Float('Điểm số')
    type = fields.Selection(
        [('theory', 'Lý thuyết'), ('practical', 'Thực hành'),
         ('both', 'Cả hai'), ('other', 'Khác')],
        'Loại', default="theory", required=True)
    subject_type = fields.Selection(
        [('compulsory', 'Bắt buộc'), ('elective', 'Tự chọn')],
        'Hình thức', default="compulsory", required=True)
    # department_id = fields.Many2one(
    #     'dsscustomers.department', 'Phòng',
    #     default=lambda self:
    #     self.env.user.dept_id and self.env.user.dept_id.id or False)
    active = fields.Boolean(default=True)

    _sql_constraints = [
        ('unique_subject_code',
         'unique(code)', 'Code should be unique per subject!'),
    ]


