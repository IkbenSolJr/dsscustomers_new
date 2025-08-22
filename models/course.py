# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DssCustomerCourse(models.Model):
    _name = "dsscustomers.course"
    _inherit = "mail.thread"
    _description = "DSS Customers Course"

    name = fields.Char('Tên', required=True)
    code = fields.Char('Code', size=16, required=True)
    parent_id = fields.Many2one('dsscustomers.course', 'Khoa học cha')
    evaluation_type = fields.Selection(
        [('normal', 'Normal'), ('GPA', 'GPA'),
         ('CWA', 'CWA'), ('CCE', 'CCE')],
        'Đánh giá', default="normal", required=True)
    max_unit_load = fields.Float("Điểm tối đa")
    min_unit_load = fields.Float("Điểm tối thiểu")
    # department_id = fields.Many2one(
    #     'op.department', 'Department',
    #     default=lambda self:
    #     self.env.user.dept_id and self.env.user.dept_id.id or False)
    active = fields.Boolean(default=True)
    subject_ids = fields.Many2many('dsscustomers.subject', string='Các Môn học')

    _sql_constraints = [
        ('unique_course_code',
         'unique(code)', 'Code should be unique per course!')]

    @api.constrains('parent_id')
    def _check_parent_id_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('Bạn không thể tạo Khóa học đệ quy.'))
        return True

    # @api.model
    # def get_import_templates(self):
    #     return [{
    #         'label': _('Import Template for Courses'),
    #         'template': '/openeducat_core/static/xls/op_course.xls'
    #     }]
