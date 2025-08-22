from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals):
        # Tạo khách hàng như bình thường
        partner = super(ResPartner, self).create(vals)

        # Nội dung ghi chú vào chatter
        checklist_url = "https://docs.google.com/spreadsheets/d/1RB2UShfa1wYxo7D8aZE7txwusXBegSMML2m-dbfacQ8/edit?sharingaction=ownershiptransfer&gid=1562386216#gid=1562386216"
        message = _("🎯 <b>Checklist xử lý hồ sơ:</b><br/>%s") % checklist_url

        # Ghi vào Chatter
        partner.message_post(
            body=message,
            message_type='comment',
            subtype_xmlid='mail.mt_note'
        )

        return partner
