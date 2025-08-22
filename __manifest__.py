# -*- coding: utf-8 -*-
{
    'name': "DSS Custumers",
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    'description': """
        Long description of module's purpose
    """,
    'author': "DSS Education",
    'website': "https://dsseducation.com",
    'category': 'Administration',
    'version': '0.1',
    'depends': ['base','hr','mail','crm','account'],
    'data': [           
        'security/dsscustomers_security.xml',
        'security/ir.model.access.csv',
        'data/data.xml', 
        # 'data/ir_cron_data.xml',
        'data/ir_cron_status.xml',
        'views/views.xml',
        'views/ketoan.xml',
        'views/duhoc.xml',
        'views/dhcom.xml',
        'views/processing.xml',
        'views/teacher.xml',
        'views/course.xml',
        'views/dssclass.xml',
        'views/registerclass.xml',
        'views/timetable.xml', 
        'views/attendance_line.xml',  
        'views/attendance_sheet.xml', 
        'views/coursework.xml',
        'views/registerclasswork.xml',
        'views/dssclasswork.xml',
        'views/teacherwork.xml',
        'views/classromdetail.xml',
        'views/attendance_session_view.xml',
        'views/subject_view.xml',
        'views/kh_active.xml',
        'views/kh_thanhly.xml',
        'views/kh_tamhoan.xml',
        # 'views/kh_dangthanhly.xml',
        'views/kh_hoanthanh.xml',
        # 'views/report.xml',
        # 'wizard/generate_timetable_view.xml',
        # 'wizard/time_table_report.xml',
        # 'wizard/session_confirmation.xml',
       
         
    ],
    'assets': {
        'web.assets_backend': [
            'dsscustomers/static/src/css/style.css',
        ],
    },
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
