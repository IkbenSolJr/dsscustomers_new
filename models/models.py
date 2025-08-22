# -*- coding: utf-8 -*-

from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError, ValidationError
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
    visa = fields.Selection([('482', '482'),('482dama', '482 DAMA'),('462', '462'),('500', '500'),('600', '600'),('186', '186'),('186dama', '186 DAMA'),('403', '403'),('407', '407'),('494', '494'),('dubai', 'Dubai'),('caworkpermit', 'Canada Work Permit'),('ca', 'Canada'),('uc', 'Úc'),('nz', 'NZ'),('laodong', 'Lao động'),('dulich', 'Du lịch'),('khac', 'Khác')], string="Loại Visa",track_visibility='onchange',default=False)
    danhgiakh = fields.Selection([('tiemnang', 'Tiềm năng'),('khongtiemnang', 'Không tiềm năng'),('lenhopdongmau', 'Đã lên hợp đồng'),('hot', 'Hot'),('kyhd', 'Ký Hợp đồng')],string="Đánh giá KH",track_visibility='onchange',default=False)
    namsinh = fields.Date(string="Ngày sinh")
    ngaychothd = fields.Date(string="Ngày chốt HĐ")
    phihopdong = fields.Monetary(string="Phí hợp đồng",currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string="Currency", compute='_compute_currency_id', store=True, readonly=False)
    nghenghiep = fields.Char(string="Nghề hiện tại")
    taichinh = fields.Char(string="Tài chính")
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
    tienganh = fields.Char(string="Tiếng Anh")
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
    gioitinh = fields.Selection([
                                ('nam', 'Nam'),
                                ('nu', 'Nữ'),
                                ],
                                string="Giới tính")
    emailkh = fields.Char(string="Email")
    phonekh = fields.Char(string="Điện thoại")
    mobile = fields.Char(string="Di động")
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
                                ('taichinhchuadu', 'Tài chính chưa đủ'), 
                                ('timhieuthem', 'Cần tìm hiểu thêm'),  
                                ('doituongdotuoilon', 'Lớn tuổi'),
                                ('doituongdungchamsoc', 'Dừng chăm sóc'),
                                ('doituongkhongphuhop', 'Đối tượng KH không phù hợp'),
                                ('doituongchamsoc', 'Đúng đối tượng, chăm sóc booking'),
                                ('lylichtpxau', 'Lý lịch tư pháp/Sức khỏe xấu'),
                                ('pitchingguithamdinh', 'KH đã gửi hồ sơ thẩm định'),
                                ('bopitching', 'Không tham gia pitching'),
                                ('thamgiareview', 'Đã tham gia trả kết quả thẩm định hồ sơ'),
                                ('guiemailofferkh', 'Đã gửi email offer cho KH'),
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
                                ('quantambhpxkld', 'Quan tâm chương trình BHP / XKLĐ'),
                                ('khac', 'Khác')    
                                ],
                                string="Trạng thái KH", default=False, track_visibility='onchange')
    nguondtkh = fields.Selection([('hotline', 'Hotline'),
                                    ('hotlinemn', 'Hotline Miền Nam'),
                                    ('hotlinemb', 'Hotline Miền Bắc'),
                                    ('hotlinemt', 'Hotline Miền Trung'),
                                    ('tiktok', 'Tiktok'),
                                    ('gmail', 'Gmail'),
                                    ('seeding', 'Seeding'),
                                    ('tructieptaivanphong', 'Trực tiếp tại văn phòng'),
                                    ('tunguoiquen', 'Từ người quen'),
                                    ('chidaisy', 'Chị Daisy'),
                                    ('facebook', 'Facebook Chính'),
                                    ('facebookads', 'Facebook Miền Trung'),
                                    ('facebookmienbac', 'Facebook Miền Bắc'),
                                    ('zalo', 'Zalo'),
                                    ('website', 'Website'),
                                    ('googleads', 'Google Ads'),                       
                                    ('lhu', 'LHU'),
                                    ('dsstraining', 'DSS Training'),
                                    ('khgioithieu', 'KH giới thiệu'),
                                    ('doitac', 'Đối tác'),
                                    ('sukien', 'Sự kiện'),                                
                                    ('nguonkhac', 'Nguồn khác')],
    string="Nguồn data",default=False)
    stt_count = fields.Char(string='Stt', required=True, copy=False, readonly=True,default=lambda self: _('New'))
    thanhpho = fields.Char(string="Tỉnh/Thành phố")
    truonghocuc = fields.Char(string="Trường học ở Úc")
    trangthaics = fields.Selection([('active', 'Đang Active'),('thanhly', 'Đã Thanh lý'),('dangthanhly', 'Đang Thanh lý'),('dahoanthanh', 'Visa Granted'),('tamhoan', 'Tạm hoãn')],string="Trạng thái CS",default=False)
    compute_checkgroups = fields.Boolean(string="check field", compute='get_user')
    #Bo sung sale
    nguondoitac = fields.Many2one(
        'res.partner', string='Đối tác cung cấp',
        states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
        change_default=True)

    nghebooking = fields.Selection([('bep', 'Bếp'),
                                ('farm', 'Farm'),
                                ('thit', 'Thịt'),
                                ('holy', 'Hộ lý'),
                                ('xaydung', 'Xây dựng'),
                                ('chebienthit', 'Chế biến thịt'),
                                ('oto', 'Ô tô'),
                                ('adgecare', 'Aged care'),
                                ('hair', 'Hair'),
                                ('thohancokhi', 'Thợ hàn, Cơ khí'),
                                ('nhahang', 'Nhà hàng khách sạn'),
                                ('thomoc', 'Thợ mộc'),
                                ('tapvu', 'Tạp vụ'),
                                ('ketoan', 'Kế toán'),
                                ('duhoc', 'Du học'),
                                ('nvkho','Nhân viên kho'),
                                ('thone','Thợ nề'),
                                ('nuoichongthuysan','Nhân viên nuôi trồng thủy hải sản'),
                                ('nongtraisx','Nhân viên nông trại sản xuất'), 
                                ('vanhanhmaynn','Nhân viên vận hành máy móc nông nghiệp'),
                                ('suathanvooto','Sửa chữa thân vỏ ô tô'), 
                                ('thohan','Thợ ốp lát, Thợ hàn'), 
                                ('spalamdep','Quản lý Spa làm đẹp'), 
                                ('thokythuat','Thợ kỹ thuật'), 
                                ('thodienlanh','Thợ điện lạnh'),
                                ('kientrucsu','Kiến trúc sư'), 
                                ('nvbanle','Nhân viên bán lẻ'), 
                                ('quantrictvada','Quản trị viên chương trình và dự án'),
                                ('tuvanmkt','Quản lý nhân viên tư vấn và marketing'), 
                                ('laptrinhvien','Lập trình viên'),
                                ('kysumang','Kỹ sư mạng'), 
                                ('thokinh','Thợ làm kính'),
                                ('bsygiadinh','Bác sỹ gia đình'), 
                                ('gvmamnon','Giáo viên mầm non'),
                                ('duhoc','Quản lý dự án xây dựng'),
                                ('khac', 'Nghề khác')], 
                                string="Nghề booking", default=False)
    quocgiabook = fields.Selection([('uc', 'Úc'),
                                ('canada', 'Canada'),
                                ('newzealand', 'New Zealand'),
                                ('dubai', 'Dubai'),
                                ('ireland', 'Ireland'),
                                ('balan', 'Ba Lan')], 
                                string="Quốc gia Book", default=False)
    noidungtele = fields.Text(string="Nội dung cuộc gọi Telesales")
    ndmeeting = fields.Text(string="Nội dung follow sau meeting")
    hocvan = fields.Selection([('tieuhoc', 'Tiểu học'),
                                ('thcs', 'THCS'),
                                ('thpt', 'THPT'),
                                ('trungcap', 'Trung cấp'),
                                ('caodang', 'Cao đẳng'),
                                ('daihoc', 'Đại học')], 
                                string="Học vấn", default=False)
    trinhdotienganh = fields.Selection([('khong', 'Không'),
                                ('coban', 'Cơ bản'),
                                ('giaotiep', 'Giao tiếp'),
                                ('ie34pte23', 'Ielts 3.0-4.0/ PTE 23+'),
                                ('ie45pte29', 'Ielts 4.0-5.0 /PTE 29+'),
                                ('ie56pte36', 'Ielts 5.0-6.0 / PTE 36+'),
                                ('ie6pte46', 'Ielts trên 6.0 / PTE 46+')], 
                                string="Trình độ tiếng anh", default=False)

    thuphidt = fields.Boolean(string='Phí đào tạo TA')
    thuphinghe = fields.Boolean(string='Phí đào tạo Nghề')
    tanhht = fields.Text(string="Tiếng Anh hiện tại")
    ngheht = fields.Text(string="Nghề hiện tại")

    def expand_tienganh(self):
        """ Trả về ID của bản ghi để JavaScript xử lý mở rộng """
        self.ensure_one()
        if not self.dangky_ids:
            raise UserError("Chưa có thông tin đào tạo Tiếng Anh!")        
        return {
            'type': 'ir.actions.act_window',
            'name': 'Thông tin đào tạo Tiếng Anh',
            'res_model': 'dsscustomers.register',
            'view_mode': 'tree,form', 
            'domain': [('sinhvien_ids', '=', self.id)],
            # 'view_id': self.env.ref('dsscustomers.view_dsscustomers_register_tree').id,
            'target': 'current',
        }

    def expand_nghe(self):
        """ Trả về ID của bản ghi để JavaScript xử lý mở rộng """
        self.ensure_one() 
        if not self.dangky_ids:
            raise UserError("Chưa có thông tin đào tạo nghề!")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Thông tin đào tạo nghề',
            'res_model': 'dsscustomers.registerwork',
            'view_mode': 'tree,form',
            'domain': [('sinhvien_ids', '=', self.id)], 
            # 'view_id': self.env.ref('dsscustomers.view_dsscustomers_registerwork_tree').id,
            'target': 'current',
        }

    #Tạo danh sach Email List chung
    def action_add_all_to_mailing_list(self):
        """Tự động thêm hoặc cập nhật khách hàng vào danh sách Email Marketing 'Khách hàng'"""
        mailing_list = self.env['mailing.list'].search([('name', '=', 'Khách hàng')], limit=1)

        if not mailing_list:
            mailing_list = self.env['mailing.list'].create({
                'name': 'Khách hàng',
                'is_public': True,
            })

        customers = self.search([('emailkh', '!=', False)])     # Lọc khách hàng có email
        for customer in customers:
            contact = self.env['mailing.contact'].search([('email', '=', customer.emailkh)], limit=1)

            if contact:
                # Nếu contact đã tồn tại, cập nhật thông tin còn thiếu
                update_vals = {}
                if not contact.name and customer.khachhang_id:
                    update_vals['name'] = customer.khachhang_id.name
                if mailing_list.id not in contact.list_ids.ids:
                    update_vals['list_ids'] = [(4, mailing_list.id)]  # Thêm vào danh sách nếu chưa có

                if update_vals:
                    contact.write(update_vals)
            else:
                # Nếu contact chưa tồn tại, tạo mới
                self.env['mailing.contact'].create({
                    'email': customer.emailkh,
                    'name': customer.khachhang_id.name if customer.khachhang_id else "Khách hàng",
                    'list_ids': [(4, mailing_list.id)],  # Thêm vào danh sách email
                })


    # Tạo danh sach Email List Nữ
    def action_add_all_female_to_mailing_list(self):
        """Tự động thêm hoặc cập nhật khách hàng vào danh sách Email Marketing 'Khách hàng'"""
        mailing_list = self.env['mailing.list'].search([('name', '=', 'Khách hàng Nữ')], limit=1)

        if not mailing_list:
            mailing_list = self.env['mailing.list'].create({
                'name': 'Khách hàng Nữ',
                'is_public': True,
            })

        customers = self.search([('emailkh', '!=', False),('gioitinh', '=', 'nu')])
        for customer in customers:
            contact = self.env['mailing.contact'].search([('email', '=', customer.emailkh)], limit=1)

            if contact:
                # Nếu contact đã tồn tại, cập nhật thông tin còn thiếu
                update_vals = {}
                if not contact.name and customer.khachhang_id:
                    update_vals['name'] = customer.khachhang_id.name
                if mailing_list.id not in contact.list_ids.ids:
                    update_vals['list_ids'] = [(4, mailing_list.id)]  # Thêm vào danh sách nếu chưa có

                if update_vals:
                    contact.write(update_vals)
            else:
                # Nếu contact chưa tồn tại, tạo mới
                self.env['mailing.contact'].create({
                    'email': customer.emailkh,
                    'name': customer.khachhang_id.name if customer.khachhang_id else "Khách hàng nữ",
                    'list_ids': [(4, mailing_list.id)],  # Thêm vào danh sách email
                })
   
   
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

    @api.model
    def create_att(self, vals):
        templates = super(dsscustomers,self).create(vals)
        for template in templates:
            if template.attachmenths_ids:
                template.attachmenths_ids.write({'res_model': self._name, 'res_id': template.id})
        return templates
            

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
                'view_mode': 'tree,form',
                'target': 'current'
            }

    def action_dsscustomers_nghe(self):        
            return {
                'type': 'ir.actions.act_window',
                'name': 'Du học nghề',
                'res_model': 'dsscustomers.processing.nghe',
                'domain': [('khachhangnghe_ids', '=', self.id)],
                'context': {'default_khachhangnghe_ids': self.id},
                'view_mode': 'tree,form',
                'target': 'current'
            }
    def action_dsscustomers_duhoc(self):        
            return {
                'type': 'ir.actions.act_window',
                'name': 'Du học nghề',
                'res_model': 'dsscustomers.processing.duhoc',
                'domain': [('khachhangdh_ids', '=', self.id)],
                'context': {'default_khachhangdh_ids': self.id},
                'view_mode': 'tree,form',
                'target': 'current'
            }

    def action_dsscustomers_ngoaingu(self):        
            return {
                'type': 'ir.actions.act_window',
                'name': 'Đào tạo tiếng Anh',
                'res_model': 'dsscustomers.register',
                'domain': [('sinhvien_ids', '=', self.id)],
                'context': {'default_sinhvien_ids': self.id},
                'view_mode': 'tree,form',
                'target': 'current'
            }



# CRM Custumer custom

class CrmCustomer(models.Model):
    _inherit = 'crm.lead' 


    def action_view_customer_dss(self): 
        DSSModel = self.env['dsscustomers.dsscustomers']        
        for lead in self:
            if not lead.partner_id:
                raise UserError(_('Bạn phải đặt tên khách hàng trước khi chuyển đổi.'))
             
            existing_record = DSSModel.search([('khachhang_id', '=', lead.partner_id.id)], limit=1)
            if existing_record:
                    raise ValidationError("Khách hàng đã tồn tại.")  


            fields_to_copy = {
                        # 'name': lead.name,
                        'khachhang_id': lead.partner_id.id,
                        'emailkh': lead.email_from,
                        'phonekh': lead.phone,
                        'mobile': lead.mobile,
                        # 'team_id': lead.team_id.id,
                        'user_id': lead.user_id.id,
                        'visa': lead.visa,
                        'diachi': lead.noio,
                        'namsinh': lead.sinhnhat,
                        'nhucaukh': lead.nhucau,
                        'nghenghiep': lead.nghenghiep,
                        'adskh': lead.adsdss,
                        'trangthaikh': lead.trangthaidt,
                        'thanhpho': lead.city,
                        'trinhdokh': lead.trinhdo,
                        'tienganh': lead.tienganh,
                        'taichinh': lead.taichinh,
                        'danhgiakh': lead.danhgiakh, 
                        'nguondtkh': lead.nguondt,
                        'nghebooking': lead.nghebooking,
                        'quocgiabook': lead.quocgiabook,
                        'noidungtele': lead.noidungtele,
                        'gioitinh': lead.gioitinh,
                        'hocvan': lead.hocvan,
                        'trinhdotienganh': lead.trinhdotienganh, 
                        'nguondoitac': lead.nguondoitac,                  
                    }

            dss_record = DSSModel.create(fields_to_copy)
            messages = self.env['mail.message'].search([
                ('model', '=', 'crm.lead'),
                ('res_id', '=', lead.id),
            ], order='create_date asc')
            for message in messages:
                message.copy({'model': 'dsscustomers.dsscustomers', 'res_id': dss_record.id})
            attachments = self.env['ir.attachment'].search([('res_model', '=', 'crm.lead'), ('res_id', '=', lead.id)])
            for attachment in attachments:
                attachment.copy({'res_model': 'dsscustomers.dsscustomers', 'res_id': dss_record.id})

            # activities = self.env['mail.activity'].search([('res_model', '=', 'crm.lead'), ('res_id', '=', lead.id)])
            # for activity in activities:
            #     activity.copy({'res_model': 'dsscustomers.dsscustomers', 'res_id': dss_record.id})

        return {
            'type': 'ir.actions.act_window',
            'name': 'Chuyển đổi thành Khách hàng DSS',
            'view_mode': 'form',
            'res_model': 'dsscustomers.dsscustomers',
            'res_id': dss_record.id,
            'target': 'current',    
        }