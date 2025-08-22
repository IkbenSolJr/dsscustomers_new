# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class DssCustomerCoursework(models.Model):
    _name = "dsscustomers.coursework"
    _inherit = "mail.thread"
    _description = "DSS Customers Course work"
    _rec_name = "name"

    name = fields.Char('Tên khóa học', required=True)
    code = fields.Char('Mã Code', size=16, required=True)
    parent_id = fields.Many2one('dsscustomers.coursework', 'Khóa học cha')
    # evaluation_type = fields.Selection(
    #     [('normal', 'Normal'), ('GPA', 'GPA'),
    #      ('CWA', 'CWA'), ('CCE', 'CCE')],
    #     'Evaluation Type', default="normal", required=True)
    # subject_ids = fields.Many2many('op.subject', string='Subject(s)')
    # max_unit_load = fields.Float("Maximum Unit Load")
    # min_unit_load = fields.Float("Minimum Unit Load")
    # department_id = fields.Many2one(
    #     'op.department', 'Department',
    #     default=lambda self:
    #     self.env.user.dept_id and self.env.user.dept_id.id or False)
    active = fields.Boolean(default=True)

    # _sql_constraints = [
    #     ('unique_course_code',
    #      'unique(code)', 'Code should be unique per course!')]

    @api.constrains('parent_id')
    def _check_parent_id_recursion(self):
        if not self._check_recursion():
            raise ValidationError(_('You cannot create recursive Course.'))
        return True

    # @api.model
    # def get_import_templates(self):
    #     return [{
    #         'label': _('Import Template for Courses'),
    #         'template': '/openeducat_core/static/xls/op_course.xls'
    #     }]
