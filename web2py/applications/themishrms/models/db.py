# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db = db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################
import os
filepath = os.path.join(request.folder,'uploads')

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
auth = Auth(db, hmac_key=Auth.get_or_create_key())
crud, service, plugins = Crud(db), Service(), PluginManager()

## create all tables needed by auth if not custom tables



auth.settings.extra_fields['auth_user']= [
	Field('organization_name','string', requires=IS_NOT_EMPTY(error_message='Organization name cannot be empty')),
	Field('location', 'string', requires=IS_NOT_EMPTY(error_message='Location name cannot be empty')),
	Field('department','string', requires=IS_NOT_EMPTY(error_message='Department name cannot be empty')),
	Field('employee_code', 'string', unique=True, requires=IS_NOT_EMPTY(error_message='Employee code cannot be empty')),
	Field('personal_email', requires=IS_EMAIL(error_message='Invalid personal email-id')),
	Field('date_of_joining', 'date', requires=IS_NOT_EMPTY(error_message='Please enter the date of joining of the employee')),
	Field('reporting_manager', 'string', requires=IS_NOT_EMPTY(error_message='Please enter the Reporting Manager name')),
	Field('designation', 'string', requires=IS_NOT_EMPTY(error_message='Please enter the employee Designation')),
	Field('employee_status', requires=IS_IN_SET(['Active','Terminated','Resigned','Leave-of-Absence','Deceased'],error_message='Please select the Employee Status')),
	Field('date_of_exit', 'date'),
	Field('exit_remark', 'text')
  ]

auth.define_tables()

## configure email
mail=auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.login_onaccept = lambda form: lgin(form)
auth.settings.logout_onlogout = lambda usr: lgout(usr)
auth.settings.actions_disabled.append('register')
auth.settings.actions_disabled.append('profile')
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth,filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

def get_org_name(c):
	row = db(db.add_new_organization.id == c).select(db.add_new_organization.organization_name).first()
	return row.organization_name

def get_dpt_name(c):
	row = db(db.add_new_department.id == c).select(db.add_new_department.department).first()
	return row.department

def get_loc_name(c):
	row = db(db.add_new_organization.id == c).select(db.add_new_organization.location).first()
	return row.location
	
def get_project_name(c):
	row = db(db.project.id == c).select(db.project.project_name).first()
	return row.project_name

def get_emp_name(c):
	row = db(db.auth_user.id == c).select(db.auth_user.email).first()
	return row.email

def get_rptmgr_name(c):
	row = db(db.auth_user.id == c).select(db.auth_user.reporting_manager).first()
	return row.reporting_manager
	
def get_promgr_name(c):
	row = db(db.auth_user.id == c).select(db.auth_user.email).first()
	return row.email	

db.define_table('add_new_organization',
				Field('organization_name','string',requires=IS_NOT_EMPTY(error_message='Please enter the Organization Name')),
				Field('organization_prefix','string',requires=IS_NOT_EMPTY(error_message='Please enter the Organization Prefix')))
				
db.define_table('add_new_department',
				Field('department','string',requires=IS_NOT_EMPTY(error_message='Please add the Department Name')),
				Field('description','string',requires=IS_NOT_EMPTY(error_message='Please add the Description of the Department Name')))

db.define_table('add_new_location',
				Field('organization_name',db.add_new_organization, represent=lambda c, row:get_org_name(c), requires = IS_IN_DB(db,'add_new_organization.id','%(organization_name)s')),
				Field('location','string',requires=IS_NOT_EMPTY(error_message='Please add the Organization Location')),
				Field('phone','integer',requires=IS_LENGTH(10)),
				Field('address','text'))

db.define_table('practice_area',
				Field('department',db.add_new_department, represent=lambda c, row:get_dpt_name(c), requires = IS_IN_DB(db,'add_new_department.id','%(department)s')),
				Field('practice_area'))
	
db.define_table('employee_login_detail',
				Field('employee_code'),
				Field('employee_email'),
				Field('employee_name'),
				Field('employee_login_date'),
				Field('employee_login_time'),
				Field('employee_logout_date',default='Logged in'), 
				Field('employee_logout_time',default='Logged in'),
				Field('total_minutes',default='Logged in'),
				Field('toal_hours',default='Logged in'),
				Field('ip_address'))

db.define_table('personal_information',
				Field('employee_code'),
				Field('email'),
				Field('date_of_birth','date',requires=IS_NOT_EMPTY(error_message = 'Please Choose your date of birth')),
				Field('gender',requires=IS_IN_SET(['Male','Female'], error_message='Please Select your Gender')),
				Field('marital_status',requires=IS_IN_SET(['Maried','Unmaried'], error_message='Please Select your Marital Status')),
				Field('blood_group',requires=IS_NOT_EMPTY(error_message='Please enter your blood group')),
				Field('mobile','integer',requires=IS_LENGTH(10)),
				Field('phone','integer',requires=IS_LENGTH(11)),
				Field('present_address','text'),
				Field('permanent_address','text'),
				Field('citizenship'),
				Field('state',requires=IS_IN_SET(['Andhra Pradesh','Arunachal Pradesh','Assam','Andaman and Nicobar Islands','Bihar','Chandigarh','Chhattisgarh','Dadar and Nagar Haveli','Daman and Diu','Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu and Kashmir','Jharkhand','Karnataka','Kerala','Lakshadeep','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Orissa','Pondicherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Tripura','Uttaranchal','Uttar Pradesh','West Bengal'], error_message='Please Select your State')),
				Field('passport_no'),
				Field('bank_account_no','integer'),
				Field('pan_card_no'))
				
db.define_table('qualification',
				Field('employee_code'),
				Field('email'),
				Field('university',requires=IS_NOT_EMPTY(error_message='Please enter the University Name')),
				Field('name_of_course',requires=IS_NOT_EMPTY(error_message='Please enter the Name of Course')),
				Field('specification'),
				Field('grade',requires=IS_NOT_EMPTY(error_message='Please enter grade')),
				Field('percentage',requires=IS_NOT_EMPTY(error_message='Please enter Percentage')),
				Field('completion_year','date',requires=IS_NOT_EMPTY(error_message='Please enter Completion Year')))
				
db.define_table('document',
				Field('employee_code'),
				Field('email'),
				Field('document_description',requires=IS_NOT_EMPTY(error_message='Please enter the description for the Document')),
				Field('document_upload','upload',uploadfolder=filepath,autodelete=True,requires=[IS_LENGTH(maxsize=1024*20480,error_message='Please Upload the file less than 20 MB'),IS_NOT_EMPTY(error_message='Please Choose the document for upload')]))
				
db.define_table('image',
				Field('employee_code'),
				Field('email'),
				Field('image','upload',uploadfolder=filepath,autodelete=True,requires=[IS_LENGTH(maxsize=1024*1024,error_message='Please Upload the file less than 1 MB'),IS_IMAGE(extensions=('jpeg','png'),error_message='Please Upload only the jpeg and png files')]))
				
db.define_table('holiday_list',
				Field('holiday_date','date',requires=IS_NOT_EMPTY(error_message='Please enter the Holiday date')),
				Field('holiday_name',requires=IS_NOT_EMPTY(error_message='Please enter the Holiday Name')),
				Field('remarks','text'))
				
db.define_table('apply_leave',
				Field('employee_code'),
				Field('email'),
				Field('name'),
				Field('leave_type',requires=IS_IN_SET(['Casual Leave','Medical Leave','Vacation Leave'], error_message='Please Select Leave type')),
				Field('from_leave','date'),
				Field('to_leave','date'),
				Field('total_day','integer'),
				Field('reason_for_leave','text'),
				Field('reporting_manager'),
				Field('approved_by'),
				Field('status',requires=IS_IN_SET(('Approved','Pending','Rejected')),default='Pending'))
				
db.define_table('employee_leave',
				Field('employee_code'),
				Field('email'),
				Field('taken_vacation_leave','integer'),
				Field('taken_medical_leave','integer'),
				Field('taken_casual_leave','integer'),
				Field('left_vacation_leave','integer'),
				Field('left_medical_leave','integer'),
				Field('left_casual_leave','integer'))

db.define_table('project',
				Field('project_name',unique=True,requires=[IS_NOT_EMPTY(error_message='Please enter the Project Name'),IS_NOT_IN_DB(db, 'project.project_name')]),
				Field('client_name',requires=IS_NOT_EMPTY(error_message='Please add the Client Name')),
				Field('company_name',requires=IS_NOT_EMPTY(error_message='Please enter the Company Name')),
				Field('company_email',requires=IS_EMAIL(error_message='Please enter the company email')),
				Field('practice_head',db.auth_user, represent=lambda c, row:get_rptmgr_name(c), requires = IS_IN_DB(db,'auth_user.id','%(reporting_manager)s')),
				Field('project_manager',db.auth_user, represent=lambda c, row:get_promgr_name(c), requires = IS_IN_DB(db,'auth_user.id','%(email)s')))

db.define_table('activity',
				Field('project_name',db.project, represent=lambda c, row:get_project_name(c), requires = IS_IN_DB(db,'project.id','%(project_name)s')),
				Field('activity'))

db.define_table('assign_project',
				Field('project_name',db.project, represent=lambda c, row:get_project_name(c), requires = IS_IN_DB(db,'project.id','%(project_name)s')), 
				Field('organization_name'),
				Field('department'),
				Field('employee'))
				
db.define_table('activity_tracker',
				Field('employee_code'),
				Field('email'),
				Field('project_name',requires=IS_NOT_EMPTY(error_message='Please add the Project Name')),
				Field('project_task',requires=IS_NOT_EMPTY(error_message='Please add the Project Name')),
				Field('task_description'),
				Field('date','date'),
				Field('total_time','integer'),
				Field('client_name',requires=IS_NOT_EMPTY(error_message='Please add the Client Name')),
				Field('company_name',requires=IS_NOT_EMPTY(error_message='Please enter the Company Name')),
				Field('company_email',requires=IS_EMAIL(error_message='Please enter the company email')),
				Field('practice_head'),
				Field('project_manager'))
