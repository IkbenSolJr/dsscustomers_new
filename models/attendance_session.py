# -*- coding: utf-8 -*-

from odoo import models, fields


class DssSession(models.Model):
    _inherit = "dsscustomers.session"

    attendance_sheet = fields.One2many('dsscustomers.attendance.sheet',
                                       'session_id', string='Session')

    def get_attendance(self, context=None):

        sheet = self.env['dsscustomers.attendance.sheet'].search(
            [('session_id', '=', self.id)])
        register = self.env['dsscustomers.attendance.sheet'].search(
            [('course_id', '=', self.course_id.id)])

        if self.id == sheet.session_id.id:
            if len(sheet) <= 1:
                view_id = self.env.ref('dsscustomers.'
                                       'view_dsscustomers_attendance_sheet_form').id,
                return {
                    'name': 'Attendance Sheet',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'views': [(view_id, 'form')],
                    'res_model': 'dsscustomers.attendance.sheet',
                    'view_id': view_id,
                    'type': 'ir.actions.act_window',
                    'target': 'current',
                    'res_id': sheet.id,
                    'context': {'default_session_id': self.id,
                                'default_register_id': [rec.id for rec in register]},
                    'domain': [('session_id', "=", sheet.session_id.id)]
                }

            action = self.env.ref('dsscustomers.'
                                  'act_open_dsscustomers_attendance_sheet_view').read()[0]
            action['domain'] = [('session_id', '=', self.id)]
            action['context'] = {
                'default_session_id': self.id,
                'default_register_id': [rec.id for rec in register]}
            return action

        else:
            view_id = self.env.ref('dsscustomers.'
                                   'view_dsscustomers_attendance_sheet_form').id,
            return {
                'name': 'Attendance Sheet',
                'view_type': 'form',
                'view_mode': 'tree',
                'views': [(view_id, 'form')],
                'res_model': 'dsscustomers.attendance.sheet',
                'view_id': False,
                'type': 'ir.actions.act_window',
                'target': 'current',
                'context': {'default_session_id': self.id,
                            'default_register_id': [rec.id for rec in register]},
                'domain': [('session_id', "=", self.id)]
            }
