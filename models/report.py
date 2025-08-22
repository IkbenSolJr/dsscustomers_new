# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP


class dsscustomers(models.Model):
    _name = 'dsscustomers.dsscustomers'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'DSS Customers'
    _rec_name = 'khachhang_id'

    thutu = fields.Char(string="STT")
    image = fields.Binary(string="Customers Image")
    khachhang_id = fields.Many2one(
        'res.partner', string='Khách hàng',
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        required=True, change_default=True,index=True, track_visibility='onchange')
    masokh = fields.Char(string="MSKH")
    visa = fields.Selection([('482', '482'),('462', '462'),('500', '500'),('600', '600'),('186', '186'),('403', '403'),('407', '407'),('dubai', 'Dubai'),('caworkpermit', 'Canada Work Permit'),('ca', 'Canada'),('uc', 'Úc'),('nz', 'NZ'),('laodong', 'Lao động'),('dulich', 'Du lịch'),('khac', 'Khác')],string="Loại Visa",default=False)
    namsinh = fields.Date(string="Ngày sinh")
    ngaychothd = fields.Date(string="Ngày chốt HĐ")
    phihopdong = fields.Monetary(string="Phí hợp đồng",currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string="Currency", compute='_compute_currency_id', store=True, readonly=False)
    nghenghiep = fields.Char(string="Nghề hiện tại")
    nghenghiepvisa = fields.Char(string="Nghề theo visa")
    diachi = fields.Char(string="Địa chỉ")
    tinhtranghs = fields.Text(string="Tình trạng Hồ sơ")
    daotaonghe = fields.Selection([('hoc', 'Học'),('thuctap', 'Thực tập')],string="Đào tạo nghề",default=False)
    trangthaihs = fields.Selection([('thuctap', 'Thực tập'),('nhanvien', 'Nhân viên'),('quanly', 'Quản lý')],string="Trạng thái",default=False)
    nguoiquanly = fields.Char(string="Người quản lý")
    bangluong = fields.Char(string="Bảng lương")
    vitricv = fields.Text(string="Vị trí công việc")
    ngayravisa = fields.Date(string="Ngày ra Visa")
    hdlaodong = fields.Text(string="Hợp đồng lao động")
    pvchulaodong = fields.Text(string="Phỏng vấn CLĐ")
    tinhtrangdaotao = fields.Text(string="Tình trạng đào tạo")
    # Đào tạo
    loptienganh= fields.Char(string="Lớp tiếng Anh")
    target = fields.Char(string="Target")
    dukientarget = fields.Date(string="Dự kiến đạt target")
    # attachmenths_ids = fields.Many2many('ir.attachment', string="Hồ sơ đính kèm")
    # Đăng ký lơp hoc tieng anh
    dangky_ids = fields.One2many('dsscustomers.register','sinhvien_ids',string="Đăng ký học Ngoại ngữ")
    # score = fields.Float(related = 'dangky_ids.score',store=True)

    # Đào tạo nghề
    dangkynghe_ids = fields.One2many('dsscustomers.registerwork','sinhvien_ids',string="Đăng ký học nghề")
    
    #Processing
    duhocinfo_ids = fields.One2many('dsscustomers.processing.duhoc', 'khachhangdh_ids',string="Thông tin du học")
    duhocngheinfo_ids = fields.One2many('dsscustomers.processing.nghe', 'khachhangnghe_ids',string="Thông tin lao động")
    #Tieng Anh
    
    
    
    # Chung    
    teamphutrach = fields.Many2one('hr.department', string="Team", default=lambda self: self.env.user.department_id, track_visibility='onchange')
    user_id = fields.Many2one('res.users', 'Sale', default=lambda self: self.env.user, track_visibility='onchange')
    usercs_id = fields.Many2one('res.users', 'Phụ trách CS', default=lambda self: self.env.user, track_visibility='onchange')
    userpro_id = fields.Many2one('res.users', 'Phụ trách Processing', default=lambda self: self.env.user, track_visibility='onchange')
    userdt_id = fields.Many2one('res.users', 'Phụ trách Đào tạo', default=lambda self: self.env.user, track_visibility='onchange')
    # userdtw_id = fields.Many2one('res.users', 'Phụ trách Đào tạo nghề', default=lambda self: self.env.user, track_visibility='onchange')
    ghichu = fields.Text(string='Ghi chú')
    # Ke toan
    cvkhachhang = fields.Char(string="CV")
    batdauhoc = fields.Date(string="Ngày bắt đầu học")
    khachhangktinfo_ids = fields.One2many('dsscustomers.ketoan','khachhangkt_ids',string="Thông tin thanh toán")
    totaltt = fields.Float(string="Đã nộp", compute="_compute_total_thanhtoan")
    # Cơ bản
    emailkh = fields.Char(string="Email")
    phonekh = fields.Char(string="Điện thoại")
    nhucaukh = fields.Char(string="Nhu cầu")
    adskh = fields.Char(string="Ads")
    trinhdokh = fields.Char(string="Trình độ")
    trangthaikh = fields.Selection([
    ('khongbatmay', 'Không bắt máy/Thuê bao (Lần 1)'),
    ('khongbatmayhai', 'Không bắt máy/Thuê bao (Lần 2)'),
    ('khongbatmayba', 'Không bắt máy/Thuê bao (Lần 3)'),
    ('khongbatmaybon', 'Không bắt máy/Thuê bao (Lần 4)'),
    ('khongbatmaynam', 'Không bắt máy/Thuê bao (Lần 5)'),
    ('khongconhucau', 'Không có nhu cầu'),
    ('hengoilai', 'Hẹn gọi lại'),
    ('trungdata', 'Trùng data'),
    ('saiso', 'Không kết nối dc/ Sai số DT/ SDT không đúng'),
    ('thamgiapitching', 'Đồng ý tham gia pitching'),
    ('daguitinzalokb', 'Đã gửi tin nhắn/Zalo kết bạn cho khách'),
    ('khongdutaichinh', 'Tài chính yếu'),    
    ('doituongdotuoilon', 'Lớn tuổi'),
    ('doituongdungchamsoc', 'Dừng chăm sóc'),
    ('doituongchamsoc', 'Đúng đối tượng, tiếp tục chăm sóc'),
    ('lylichtpxau', 'Lý lịch tư pháp/Sức khỏe xấu'),
    ('pitchingguithamdinh', 'KH đã gửi hồ sơ thẩm định'),
    ('bopitching', 'Không tham gia pitching'),
    ('thamgiareview', 'Đã tham gia review'),
    ('guiemailhd', 'Đã gửi email hợp đồng cho KH'),
    ('thamgiadgenglish', 'Đã tham gia đánh giá Tiếng Anh'),
    ('follownganhan', 'Follow ngắn hạn(dưới 1 tháng)'),
    ('followdaihan', 'Follow dài hạn(từ 1 tháng trở lên)'),
    ('deposit', 'Deposit'),
    ('tiemnangkyhd', 'Tiềm năng ký hợp đồng'),    
    ('dakyhdttmot', 'Ký hợp đồng - Đã thanh toán giai đoạn 1'),
    ('ttlanhai', 'Ký hợp đồng - Đã thanh toán giai đoạn 2'),
    ('daxeplopta', 'Đã xếp lớp Tiếng Anh'),
    ('daxeplopdtn', 'Đã xếp lớp đào tạo nghề'),
    ('daotaopv', 'Đào tạo phỏng vấn'),
    ('ttlanba', 'Thanh toán lần 3'),
    ('ttlanbon', 'Thanh toán lần 4'),
    ('ttlannam', 'Thanh toán lần 5'),
    ('ttlanlansau', 'Thanh toán lần 6'),
    ('ttlanbay', 'Thanh toán lần 7')],
    string="Trạng thái KH", default=False, track_visibility='onchange')
    nguondtkh = fields.Selection([('hotline', 'Hotline'),('tiktok', 'Tiktok'),('gmail', 'Gmail'),('seeding', 'Seeding'),('tructieptaivanphong', 'Trực tiếp tại văn phòng'),('tunguoiquen', 'Từ người quen'),('chidaisy', 'Chị Daisy'),('facebook', 'Facebook'),('zalo', 'Zalo'),('dsstraining', 'DSS Training'),('khgioithieu', 'KH giới thiệu'),('doitac', 'Đối tác'),('sukien', 'Sự kiện'),('nguonkhac', 'Nguồn khác')],string="Nguồn data",default=False)
    stt_count = fields.Char(string='Stt', required=True, copy=False, readonly=True,default=lambda self: _('New'))
    thanhpho = fields.Char(string="Tỉnh/Thành phố")
    truonghocuc = fields.Char(string="Trường học ở Úc")
    trangthaics = fields.Selection([('active', 'Đang Active'),('thanhly', 'Đã Thanh lý'),('dangthanhly', 'Đang Thanh lý'),('dahoanthanh', 'Đã hoàn thành'),('tamhoan', 'Tạm hoãn')],string="Trạng thái CS",default=False)
    compute_checkgroups = fields.Boolean(string="check field", compute='get_user')
    
    #STT
    @api.model
    def create(self, vals):
        if vals.get('stt_count', _('New')) == _('New'):
           vals['stt_count'] = self.env['ir.sequence'].next_by_code('dsscustomers.dsscustomers') or _('New')
        res = super(dsscustomers, self).create(vals)
        return res

    @api.depends('khachhangktinfo_ids.sotientt')
    def _compute_total_thanhtoan(self):
        for record in self:
            record.totaltt = sum(record.khachhangktinfo_ids.mapped('sotientt'))


    @api.depends('khachhang_id')
    def _compute_currency_id(self):
        for pay in self:
            pay.currency_id = pay.khachhang_id.currency_id or pay.khachhang_id.company_id.currency_id


    @api.depends('compute_checkgroups')
    def get_user(self):
        res_user = self.env['res.users'].search([('id', '=', self._uid)])
        if res_user.has_group('dsscustomers.group_dsscustomers_sale_user') or res_user.has_group('dsscustomers.group_dsscustomers_cs_user') or res_user.has_group('dsscustomers.group_dsscustomers_processing_user') or res_user.has_group('dsscustomers.group_dsscustomers_ketoan_user'):
            self.compute_checkgroups = True
        else:
            self.compute_checkgroups = False

    # @api.model
    # def create_att(self, vals):
    #     templates = super(dsscustomers,self).create(vals)
    #     for template in templates:
    #         if template.attachmenths_ids:
    #             template.attachmenths_ids.write({'res_model': self._name, 'res_id': template.id})
    #     return templates
            

    @api.model
    def create_att(self, vals_list):
        templates = super().create(vals_list)
        for template in templates:
            if template.attachmenths_ids:
                template.attachmenths_ids.write({'res_model': self._name, 'res_id': template.id})
        return templates
            
    def action_dsscustomers_ketoan(self):        
            return {
                'type': 'ir.actions.act_window',
                'name': 'Tiến độ thanh toán',
                'res_model': 'dsscustomers.ketoan',
                'domain': [('khachhangkt_ids', '=', self.id)],
                'context': {'default_khachhangkt_ids': self.id},
                'view_mode': 'tree',
                'target': 'current'
            }

    def action_dsscustomers_nghe(self):        
            return {
                'type': 'ir.actions.act_window',
                'name': 'Du học nghề',
                'res_model': 'dsscustomers.processing.nghe',
                'domain': [('khachhangnghe_ids', '=', self.id)],
                'context': {'default_khachhangnghe_ids': self.id},
                'view_mode': 'tree',
                'target': 'current'
            }
    def action_dsscustomers_duhoc(self):        
            return {
                'type': 'ir.actions.act_window',
                'name': 'Du học nghề',
                'res_model': 'dsscustomers.processing.duhoc',
                'domain': [('khachhangdh_ids', '=', self.id)],
                'context': {'default_khachhangdh_ids': self.id},
                'view_mode': 'tree',
                'target': 'current'
            }

# CRM Custumer custom

class CrmCustomer(models.Model):
    _inherit = 'crm.lead'

    def action_view_customer_dss(self):        
            return {
                'type': 'ir.actions.act_window',
                'name': 'Khách hàng',
                'res_model': 'dsscustomers.dsscustomers',
                'domain': [('khachhang_id', '=', self.id)],
                'context': {'search_default_opportunity_id': self.id,
                            'default_opportunity_id': self.id,
                            'default_khachhang_id': self.partner_id.id,
                            'default_namsinh': self.sinhnhat,
                            'default_diachi': self.noio,
                            'default_visa': self.visa,
                            'default_emailkh': self.email_from,
                            'default_phonekh': self.phone,
                            'default_nhucaukh': self.nhucau,
                            'default_nghenghiep': self.nghenghiep,
                            'default_adskh': self.adsdss,
                            'default_trangthaikh': self.trangthaidt,
                            'default_thanhpho': self.city,
                            'default_trinhdokh': self.trinhdo,
                            'default_user_id': self.user_id.id,
                            'default_nguondtkh': self.nguondt},
                'view_mode': 'form',
                'target': 'current',
            }
