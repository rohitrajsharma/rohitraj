# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html
    """
    response.flash = "Welcome to Themis Lexsol"
    return dict(message=T('Hello World'))
	
	
def tlscareer():
    return dict()

def tlsabout():
    return dict()
    
def rt():
    return dict()

def employee():
    return dict()
    
def tlsservice():
    return dict()


def tlsoo():
    return dict()   

def tlsleads():
    return dict()   

def tlsoteam():	
	 return dict()
	 

def tlscontact(): 
    use_recaptcha = True 
    form = SQLFORM.factory(Field('Name',requires=IS_NOT_EMPTY()),Field ('your_email',requires=IS_EMAIL()),Field('your_message','text')) 
    return dict(form=form)
		
def tlscareer(): 
    form = SQLFORM.factory(Field('name',requires=IS_NOT_EMPTY()),
    								Field ('your_email',requires=IS_EMAIL()),
    								SQLField('contact_details',requires=IS_NOT_EMPTY()),
    								Field('your_message','text'),
    								SQLField('looking_for_position',requires=IS_IN_SET(['Admin', 'Legal', 'Finance','IT'])),
    								SQLField('your_resume','upload')) 
    if form.accepts(request,session):
    	session.name = form.vars.name
    	#careermail() 
    return dict(form=form)	
		
def careermail():
    from gluon.tools import Mail
    mail = Mail()
        #specify server
    mail=auth.settings.mailer
    mail.settings.server = 'smtp.gmail.com:587'
    #specify address to send as
    mail.settings.sender = 'themisdemo1@gmail.com'
    mail.settings.login = 'themisdemo1@gmail.com:123456asdfg'
    #send the message                             
    mail.send(to=['sanjeet.tls@gmail.com','prakhar.tls@gmail.com'],
            subject='Welcome User',
            message='<html>'
                        '<body>'
                            '<span style="font-family: Bodoni MT Ultra Bold;color:  #000000 ;font-size : 18pt;"><b>Themis </span></h1><span style="font-family: Bodoni MT Ultra Bold;color:#C7A317   ;font-size :18pt;"><b>Lexsol</b></span>'
                            
                            '<p>Dear &nbsp;'+session.name+'</p>'
                            
                            '<p>I just wanted to drop you a quick message to say thank you for joining the LCM Plus. I appreciate you taking the time to register and really look forward to reading your compliances. Your user name is '+session.mail+' and please click below to reset your password.<h1>http://jmdlcmplus.fluxflex.com/jmdlcmplus/default/user/request_reset_password</h1>If you need help at any time, please contact me by replying to this message. Similarly, if you ever have any questions then please do not hesitate to send me a message or email.</p>'
                            '<center><p>_________________________________________________________</p><p style="color:red;font-size :5pt;">This email comes to you since your company has subcribed for LCM Plus. TO unsubcribed please contact to your Compliance Manager</p></center>'
                      
                        '</body>'
                    '</html>'
                    
  )
    response.flash='mail send'
    return ''

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request,db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
    
def welcome():
	""" First page to be visited after installation. Will create necessary roles and permissions for admin and redirects to index."""
	create_user()
	create_group()
	create_membership()
	create_permission()
	session.flash = "Welcome to Themis"
	redirect(URL(c='default', f='index'))
	
def create_user():
	 username = 'admin'
	 password = username
	 if 'username' in auth.settings.table_user.fields():
	 	userkey = 'username'
	 elif 'email' in auth.settings.table_user.fields():
	 	userkey = 'email'
	 	username = username + '@themislexsol.com'
	 passfield = auth.settings.password_field 
	 user = db(auth.settings.table_user[userkey] == username).select().first()
	 if not user:
	 	user_id = db.auth_user.insert(**{userkey:username,passfield:CRYPT(auth.settings.hmac_key)(password)[0]})
	 	user = auth.settings.table_user(user_id)
	 return user
	 
def create_group():
    group = db(auth.settings.table_group.role == 'Admin').select().first()
    if not group:
        group_id = auth.add_group(role = 'Admin', description = 'All Permissions')
        group = auth.settings.table_group(group_id)
    return group
    
def create_membership():
	group = db(db.auth_group.role == 'Admin').select().first()
	user = db(db.auth_user.email == 'admin@themislexsol.com').select().first()
	membership = db(auth.settings.table_membership.group_id == group.id).select().first()
	if not membership:
		membership_id = auth.add_membership(group_id = group.id, user_id = user.id)
		membership = auth.settings.table_membership(membership_id)
	return membership
	
def create_permission():
	tables = list(db.tables)
	for table in tables:
		group = db(db.auth_group.role == 'Admin').select().first()
		query = auth.settings.table_permission.group_id == group.id
		query = query & (auth.settings.table_permission.name == 'CRUD')
		query = query & (auth.settings.table_permission.table_name == table)
		permission = db(query).select().first()
		if not permission:
			permission_id = auth.add_permission(group_id = group.id, name = 'CRUD', table_name = table)
			permission = auth.settings.table_permission(permission_id)
	return permission
	
def lgin(form):
	if auth.user.email == 'admin@themislexsol.com':
		admin=db(db.image.email==auth.user.email).select().first()
		if not admin:
			db.image.insert(email=auth.user.email)
			redirect(URL(c='default', f='admindash'))
		else:
			redirect(URL(c='default', f='admindash'))			
	else:
		redirect(URL(c='default', f='emp_time'))
	return dict()
	
def lgout(usr):
	if auth.user.email == 'admin@themislexsol.com':
		pass
	else:
		import datetime
		import time, os
		os.environ['TZ'] = 'Asia/Kolkata'
		time.tzset()
		currentdate=datetime.date.today()
		now = time.localtime(time.time())
		endtime=datetime.datetime.now()
		starttime = session.starttime
		delta = (endtime - starttime)
		totalminutes = str(delta.seconds / 60)
		totalhours = str(delta.seconds / 3600)
		totmin = totalminutes + '\t min'
		tothr = totalhours + '\t hrs'
		currenttime = time.strftime("%H:%M:%S", now)
		db((db.employee_login_detail.employee_email == auth.user.email) & (db.employee_login_detail.employee_login_date == currentdate) & (db.employee_login_detail.employee_login_time == session.cutime)).update(employee_logout_date=currentdate, employee_logout_time=currenttime, total_minutes=totmin, toal_hours=tothr)
		db.commit()
	return dict()

#### Admin Controller Starts from here ####	
	
@auth.requires(auth.login() and auth.has_permission('CRUD', 'auth_user'))    
def admindash():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	return dict(images=images)	 

@auth.requires_permission('CRUD', 'auth_user')		
def admin_organization():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	db.add_new_organization.id.readable = False
	form=SQLFORM.grid(db.add_new_organization, selectable = lambda ids: del_org(ids))
	return dict(images=images,form=form)
	
@auth.requires_permission('CRUD', 'auth_user')	
def del_org(ids):
	if not ids:
		response.flash='Please Select the Check-box to Delete'
	else:
		for row in ids:
			db(db.add_new_organization.id == row).delete()
		pass
	pass
	return ''
	
@auth.requires_permission('CRUD', 'auth_user')		
def admin_location():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	db.add_new_location.id.readable = False
	form=SQLFORM.grid(db.add_new_location, selectable = lambda ids: del_loc(ids))
	return dict(images=images,form=form)
	
@auth.requires_permission('CRUD', 'auth_user')	
def del_loc(ids):
	if not ids:
		response.flash='Please Select the Check-box to Delete'
	else:
		for row in ids:
			db(db.add_new_location.id == row).delete()
		pass
	pass
	return ''
	
@auth.requires_permission('CRUD', 'auth_user')		
def admin_department():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	db.add_new_department.id.readable = False
	form=SQLFORM.grid(db.add_new_department, selectable = lambda ids: del_dpt(ids))
	return dict(images=images,form=form)
	
@auth.requires_permission('CRUD', 'auth_user')	
def del_dpt(ids):
	if not ids:
		response.flash='Please Select the Check-box to Delete'
	else:
		for row in ids:
			db(db.add_new_department.id == row).delete()
		pass
	pass
	return ''

@auth.requires_permission('CRUD', 'auth_user')	
def locn(): 
	org = request.vars.org
	loc = db(db.add_new_location.organization_name == org).select()
	return SELECT(_id="locn",_name="locn",*[OPTION(loc [i].location, _value=str (loc[i].location)) for i in range(len(loc))])

@auth.requires_permission('CRUD', 'auth_user')	  
def admin_newuser():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	db.auth_user.id.readable = False
	form=SQLFORM.grid(db.auth_user, create=False, selectable = lambda ids: del_emp(ids))
	return dict(images=images,form=form)
	
@auth.requires_permission('CRUD', 'auth_user')	
def del_emp(ids):
	if not ids:
		response.flash='Please Select the Check-box to Delete'
	else:
		for row in ids:
			db(db.auth_user.id == row).delete()
		pass
	pass
	return ''

@auth.requires_permission('CRUD', 'auth_user')	
def admin_create_new_user():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	
	admin_create_new_user.count=0
	def counting():
		for row in db(db.auth_user.id >= 1).select():
			admin_create_new_user.count += 1
	counting()
	count=admin_create_new_user.count
	prefix='00'
	pre='0'
	pr=''
	if count < 10:
		id=prefix+str(count)
	elif count >= 10 and count <= 99:
		id=pre+str(count)
	else:
		id=pr+str(count)
		
	org = db().select(db.add_new_organization.ALL)
	dpt = db().select(db.add_new_department.ALL)
	rmgr = db().select(db.auth_user.ALL)
	stat = ['Active','Terminated','Resigned','Leave-of-Absence','Deceased']
	
	if request.vars.mailerror:
		var = 'This email ('+request.vars.mailerror+') is allready taken. Please choose another email address.'
	elif request.vars.mailerr:
		var = 'This email ('+request.vars.mailerr+') is Successfully Registered with HRMS.'
	else:
		var = 'Add New Employee'
	return dict(images=images, org=org, dpt=dpt, stat=stat, id=id, var=var,rmgr=rmgr)
	
@auth.requires_permission('CRUD', 'auth_user')	
def admin_submit_newuser():
	for row in db(db.auth_user.email==request.vars.orgemail).select():
		session.regmail=row.email
		pass
	if session.regmail == request.vars.orgemail:
		redirect(URL(c='default', f='admin_create_new_user', vars={'mailerror' :request.vars.orgemail}))
	else:
		session.mail = request.vars.orgemail
		session.pmail = request.vars.pemail
		session.fname = request.vars.fname
		session.mgr = request.vars.rmgr
		for row1 in db(db.add_new_organization.id==request.vars.org).select():
			pr = row1.organization_prefix
			cmpny = row1.organization_name
		prefix = str(pr+request.vars.empcode)
		db.auth_user.bulk_insert([{'first_name' : session.fname,'last_name' : request.vars.lname,'email' : session.mail,'password' : db.auth_user.password.validate('1234')[0],'organization_name' : cmpny, 'location' : request.vars.locn, 'department' : request.vars.dpt, 'employee_code' : prefix, 'personal_email' : session.pmail, 'date_of_joining' : request.vars.doj, 'reporting_manager' : request.vars.rmgr, 'designation' : request.vars.dgn, 'employee_status' : request.vars.stat}])
		create_emp_group()
		create_emp_membership()
		create_emp_permission()
		create_mgr_group()
		create_mgr_membership()
		create_mgr_permission()
		db.personal_information.insert(email=session.mail,employee_code=prefix)
		db.image.insert(email=session.mail,employee_code=prefix)
		
		totvacationleave=18
		totmedicalleave=6
		totcasualleave=6
		import datetime
		month = datetime.datetime.now().month
		totmonth = 12
		curmnth = totmonth - month
		vacleave = int(curmnth * 1.5)
		medleave = int(curmnth * 0.5)
		casulleave = int(curmnth * 0.5)
		tackenvacleave = 0
		tackenmedleave = 0
		takencasulleave = 0
		db.employee_leave.insert(employee_code=prefix,email=session.mail,taken_vacation_leave=tackenvacleave,taken_medical_leave=tackenmedleave,taken_casual_leave=takencasulleave,left_vacation_leave=vacleave,left_medical_leave=medleave,left_casual_leave=casulleave)
		db.commit()
		welcome_mail()
		redirect(URL(c='default', f='admin_create_new_user', vars={'mailerr' :request.vars.orgemail}))
	return dict()
	
@auth.requires_permission('CRUD', 'auth_user')
def welcome_mail():
    from gluon.tools import Mail
    mail=Mail()
    #specify server
    
    mail=auth.settings.mailer
    mail.settings.server='smtp.gmail.com:587'
    mail.settings.login='themisdemo1@gmail.com:123456asdfg'
    #specify address to send as
    mail.settings.sender='themisdemo1@gmail.com'
    #send the message                             
    mail.send(to=[session.mail, session.pmail],
            subject='Welcome User',
            message='<html>'
                        '<body>'
                            '<span style="font-family: Bodoni MT Ultra Bold;color:  #000000 ;font-size : 18pt;"><b>Themis </span></h1><span style="font-family: Bodoni MT Ultra Bold;color:#C7A317   ;font-size :18pt;"><b>Lexsol</b></span>'
                            
                            '<p>Dear &nbsp;'+session.fname+'</p>'
                            
                            '<p>I just wanted to drop you a quick message to say thank you for joining the Themis Lexsol.Your user name is '+session.mail+' and please click below to reset your password.<h1>http://jmdlcmplus.fluxflex.com/jmdlcmplus/default/user/request_reset_password</h1>If you need help at any time, please contact me by replying to this message. Similarly, if you ever have any questions then please do not hesitate to send me a message or email.</p>'
                            '<center><p>_________________________________________________________</p><p style="color:red;font-size :5pt;">This email comes to you since your company has subcribed for LCM Plus. TO unsubcribed please contact to Themis Lexsol</p></center>'
                      
                        '</body>'
                    '</html>'
                    
  )
    response.flash='mail send'
    return ''	
	
@auth.requires_permission('CRUD', 'auth_user')    
def create_emp_group():
    group = db(auth.settings.table_group.role == 'Emp').select().first()
    if not group:
        group_id = auth.add_group(role = 'Emp', description = 'Only Employee Permissions')
        group = auth.settings.table_group(group_id)
    return group

@auth.requires_permission('CRUD', 'auth_user')    
def create_emp_membership():
	group = db(db.auth_group.role == 'Emp').select().first()
	user = db(db.auth_user.email == session.mail).select().first()
	membership = db((auth.settings.table_membership.group_id == group.id) & (auth.settings.table_membership.user_id == user.id)).select().first()
	if not membership:
		membership_id = auth.add_membership(group_id = group.id, user_id = user.id)
		membership = auth.settings.table_membership(membership_id)
	return membership

@auth.requires_permission('CRUD', 'auth_user')	
def create_emp_permission():
	group = db(db.auth_group.role == 'Emp').select().first()
	query = auth.settings.table_permission.group_id == group.id
	query = query & (auth.settings.table_permission.name == 'Emp')
	permission = db(query).select().first()
	if not permission:
		permission_id = auth.add_permission(group_id = group.id, name = 'Emp', table_name = 'auth_user')
		permission = auth.settings.table_permission(permission_id)
	return permission
	
@auth.requires_permission('CRUD', 'auth_user')    
def create_mgr_group():
    group = db(auth.settings.table_group.role == 'Mgr').select().first()
    if not group:
        group_id = auth.add_group(role = 'Mgr', description = 'Only Manager Permissions')
        group = auth.settings.table_group(group_id)
    return group

@auth.requires_permission('CRUD', 'auth_user')    
def create_mgr_membership():
	group = db(db.auth_group.role == 'Mgr').select().first()
	user = db(db.auth_user.email == session.mgr).select().first()
	membership = db((auth.settings.table_membership.group_id == group.id) & (auth.settings.table_membership.user_id == user.id)).select().first()
	if not membership:
		membership_id = auth.add_membership(group_id = group.id, user_id = user.id)
		membership = auth.settings.table_membership(membership_id)
	return membership

@auth.requires_permission('CRUD', 'auth_user')	
def create_mgr_permission():
	group = db(db.auth_group.role == 'Mgr').select().first()
	query = auth.settings.table_permission.group_id == group.id
	query = query & (auth.settings.table_permission.name == 'Mgr')
	permission = db(query).select().first()
	if not permission:
		permission_id = auth.add_permission(group_id = group.id, name = 'Mgr', table_name = 'auth_user')
		permission = auth.settings.table_permission(permission_id)
	return permission

@auth.requires_permission('CRUD', 'auth_user')	
def admin_newholiday():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	db.holiday_list.id.readable=False
	form=SQLFORM.grid(db.holiday_list, selectable = lambda ids: del_hlist(ids))
	return dict(images=images,form=form)
	
@auth.requires_permission('CRUD', 'auth_user')	
def del_hlist(ids):
	if not ids:
		response.flash='Please Select the Check-box to Delete'
	else:
		for row in ids:
			db(db.holiday_list.id == row).delete()
		pass
	pass
	return ''

@auth.requires_permission('CRUD', 'auth_user')    
def addthemis():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	return dict(images=images)

@auth.requires_permission('CRUD', 'auth_user')	
def admin_timesheet():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	db.activity_tracker.id.readable=False
	form=SQLFORM.grid(db.activity_tracker, selectable = lambda ids: del_activity_tracker(ids))
	return dict(images=images,form=form)
	
@auth.requires_permission('CRUD', 'auth_user')	
def del_activity_tracker(ids):
	if not ids:
		response.flash='Please Select the Check-box to Delete'
	else:
		for row in ids:
			db(db.activity_tracker.id == row).delete()
		pass
	pass
	return ''	
	
@auth.requires_permission('CRUD', 'auth_user')	
def admin_attendance():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	db.employee_login_detail.id.readable=False
	form=SQLFORM.grid(db.employee_login_detail, selectable = lambda ids: del_att(ids))
	return dict(form=form,images=images)
	
@auth.requires_permission('CRUD', 'auth_user')	
def del_att(ids):
	if not ids:
		response.flash='Please Select the Check-box to Delete'
	else:
		for row in ids:
			db(db.employee_login_detail.id == row).delete()
		pass
	pass
	return ''

@auth.requires_permission('CRUD', 'auth_user')		
def admin_report():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	return dict(images=images)

@auth.requires_permission('CRUD', 'auth_user')    
def admin_mydoc():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	return dict(images=images)

@auth.requires_permission('CRUD', 'auth_user')		
def admin_salary():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	return dict(images=images)
	
@auth.requires_permission('CRUD', 'auth_user')
def admin_update_image():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
		ecode=row.employee_code
		mail=row.email
			
	db.image.email.writable=False
	db.image.employee_code.writable=db.image.employee_code.readable=False
	db.image.email.default=mail
	form=SQLFORM(db.image)
	if form.accepts(request.vars, session):
		img = form.vars.image
		db(db.image.email == auth.user.email).update(image=img)
		redirect(URL(c='default', f='admindash'))
	return dict(images=images,form=form)

@auth.requires_permission('CRUD', 'auth_user')	
def admin_calendar():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	caland=db().select(db.holiday_list.ALL)
	return dict(images=images,rows=caland)

@auth.requires_permission('CRUD', 'auth_user')	
def admin_calread():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	record = db.holiday_list(request.args(0)) or redirect(URL('error'))
	form=crud.read(db.holiday_list,record)
	return dict(form=form,images=images)
    
@auth.requires_permission('CRUD', 'auth_user')	
def admin_leave_stat():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	adminleave=db().select(db.apply_leave.ALL)
	return dict(images=images,adminleave=adminleave)

@auth.requires_permission('CRUD', 'auth_user')		
def admin_edit_leave():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	for row in db(db.apply_leave.id==request.args(0)).select():
		id=row.id
		eid=row.employee_code
		estat=row.status
		eltype=row.leave_type
		efrom=row.from_leave
		eto=row.to_leave
		ereason=row.reason_for_leave
		etotday=row.total_day
	return dict(id=id,images=images,eid=eid,estat=estat,eltype=eltype,efrom=efrom,eto=eto,ereason=ereason,etotday=etotday)

@auth.requires_permission('CRUD', 'auth_user')	
def admin_approve_leave():
	for row in db(db.apply_leave.id==request.args(0)).select():
		session.lmail=row.email
		session.empname=row.name
		session.efrom=row.from_leave
		session.eto=row.to_leave
		session.status=request.vars.status
		session.ltype=row.leave_type
		session.tday=row.total_day
	if session.status == 'Approved':
		if session.ltype == 'Casual Leave':
			for row in db(db.employee_leave.email==session.lmail).select():
				totday=row.left_casual_leave - session.tday
			db(db.apply_leave.id==request.args(0)).update(status=session.status, approved_by='Administrator')
			db(db.employee_leave.email==session.lmail).update(taken_casual_leave=session.tday,left_casual_leave=totday)
			db.commit()
			redirect(URL(c='default', f='admin_leave_mail'))
		elif session.ltype == 'Medical Leave':
			for row in db(db.employee_leave.email==session.lmail).select():
				totday=row.left_medical_leave - session.tday
			db(db.apply_leave.id==request.args(0)).update(status=session.status, approved_by='Administrator')
			db(db.employee_leave.email==session.lmail).update(taken_medical_leave=session.tday,left_medical_leave=totday)
			db.commit()
			redirect(URL(c='default', f='admin_leave_mail'))
		elif session.ltype == 'Vacation Leave':
			for row in db(db.employee_leave.email==session.lmail).select():
				totday=row.left_vacation_leave - session.tday
			db(db.apply_leave.id==request.args(0)).update(status=session.status, approved_by='Administrator')
			db(db.employee_leave.email==session.lmail).update(taken_vacation_leave=session.tday,left_vacation_leave=totday)
			db.commit()
			redirect(URL(c='default', f='admin_leave_mail'))
		else:
			pass
	else:
		db(db.apply_leave.id==request.args(0)).update(status=session.status, approved_by='Administrator')
		db.commit()
		redirect(URL(c='default', f='admin_leave_mail'))
	return ''

@auth.requires_permission('CRUD', 'auth_user')
def admin_edit_leave_status():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
	ltype=['Casual Leave','Medical Leave','Vacation Leave']
	session.eleaveid=request.args(0)
	for row in db(db.apply_leave.id==session.eleaveid).select():
		ecode=row.employee_code
		name=row.name
		fle=row.from_leave
		tle=row.to_leave
		tday=row.total_day
		rle=row.reason_for_leave
		eltype=row.leave_type
	return dict(ltype=ltype,images=images,ecode=ecode,name=name,fle=fle,tle=tle,tday=tday,rle=rle,eltype=eltype)

@auth.requires_permission('CRUD', 'auth_user')	
def admin_submit_edit_leave_status():
	db(db.apply_leave.id == session.eleaveid).update(name=request.vars.name, leave_type=request.vars.ltype, from_leave=request.vars.fleave, to_leave=request.vars.tleave, total_day=request.vars.tday, reason_for_leave=request.vars.rleave)
	db.commit()
	redirect(URL(c='default',f='admin_leave_stat'))
	return ''

@auth.requires_permission('CRUD', 'auth_user')
def admin_leave_mail():
    from gluon.tools import Mail
    mail=Mail()
    #specify server
    mail=auth.settings.mailer
    mail.settings.server='smtp.gmail.com:587'
    mail.settings.login='themisdemo1@gmail.com:123456asdfg'
    #specify address to send as
    mail.settings.sender='themisdemo1@gmail.com'
    #send the message                             
    mail.send(to=[session.lmail],
            subject='Leave Status',
            message='<html>'
                        '<body>'
                            '<span style="font-family: Bodoni MT Ultra Bold;color:  #000000 ;font-size : 18pt;"><b>Themis </span></h1><span style="font-family: Bodoni MT Ultra Bold;color:#C7A317   ;font-size :18pt;"><b>Lexsol</b></span>'
                            
                            '<p>Dear &nbsp;'+session.empname+'</p>'
                            
                            '<p>I just wanted to drop you a quick message to say Your leave request from '+str(session.efrom)+' to '+str(session.eto)+' is '+session.status+' If you need help at any time, please contact me by replying to this message. Similarly, if you ever have any questions then please do not hesitate to send me a message or email.</p>'
                            '<center><p>_________________________________________________________</p><p style="color:red;font-size :5pt;">This email comes to you since you are subcribed for HRMS. TO unsubcribed please contact to Themis Lexsol</p></center>'
                      
                        '</body>'
                    '</html>'
                    
  )
    redirect(URL(c='default', f='admin_cnf_leave'))	
    return ''
    
@auth.requires_permission('CRUD', 'auth_user')	
def admin_cnf_leave():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
	return dict(images=images,status=session.status,efrom=session.efrom,eto=session.eto,empname=session.empname)
	
@auth.requires_permission('CRUD', 'auth_user')	
def admin_contact_detail():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
	return dict(images=images)

@auth.requires_permission('CRUD', 'auth_user')	
def admin_add_project():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
	
	db.project.id.readable = False
	form=SQLFORM.grid(db.project,selectable = lambda ids: del_pro(ids))
	return dict(images=images,form=form)
	
@auth.requires_permission('CRUD', 'auth_user')	
def del_pro(ids):
	if not ids:
		response.flash='Please Select the Check-box to Delete'
	else:
		for row in ids:
			db(db.project.id == row).delete()
		pass
	pass
	return ''
	
@auth.requires_permission('CRUD', 'auth_user')	
def admin_activity():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
	
	db.activity.id.readable = False
	form=SQLFORM.grid(db.activity,selectable = lambda ids: del_activity(ids))
	return dict(images=images,form=form)
	
@auth.requires_permission('CRUD', 'auth_user')	
def del_activity(ids):
	if not ids:
		response.flash='Please Select the Check-box to Delete'
	else:
		for row in ids:
			db(db.activity.id == row).delete()
		pass
	pass
	return ''
	
@auth.requires_permission('CRUD', 'auth_user')
def admin_assign_project():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
	
	db.assign_project.id.readable=False
	form=SQLFORM.grid(db.assign_project,selectable = lambda ids: del_assign_project(ids))
	return dict(images=images,form=form)

@auth.requires_permission('CRUD', 'auth_user')	
def del_assign_project(ids):
	if not ids:
		response.flash='Please Select the Check-box to Delete'
	else:
		for row in ids:
			db(db.assign_project.id == row).delete()
		pass
	pass
	return ''
	
@auth.requires_permission('CRUD', 'auth_user')
def admin_assign_pro():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
	proj=db().select(db.project.ALL)
	orzn=db().select(db.add_new_organization.ALL)
	dept=db().select(db.add_new_department.ALL)
	return dict(images=images,proj=proj,orzn=orzn,dept=dept)
	
@auth.requires_permission('CRUD', 'auth_user')	
def admin_orz():
	for row in db(db.add_new_organization.id == request.vars.orz).select():
		organization=row.organization_name
	for row1 in db(db.add_new_department.id == request.vars.dp).select():
		department=row1.department
	
	usr=[]
	for row in db((db.auth_user.department == department) & (db.auth_user.organization_name == organization)).select():
		usr.append(row.email)
	return SELECT(_id="usr",_name="usr",*[OPTION((emp), _value=str (emp)) for emp in usr])
	
@auth.requires_permission('CRUD', 'auth_user')	
def admin_submit_project():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
	for row in db(db.add_new_organization.id == request.vars.orz).select():
		organization=row.organization_name
	for row1 in db(db.add_new_department.id == request.vars.dp).select():
		department=row1.department
	db.assign_project.insert(project_name=request.vars.pro,organization_name=organization,department=department,employee=request.vars.usr)
	db.commit()
	redirect(URL(c='default',f='admin_assign_project'))
	return dict(images=images)
	
#### Employee Controller Starts from here ####

def emp_time():
	import datetime
	import time, os
	os.environ['TZ'] = 'Asia/Kolkata'
	time.tzset()
	now = time.localtime(time.time())
	session.cutime = time.strftime("%H:%M:%S", now)	
	redirect(URL(c='default',f='employee'))
	return ''

@auth.requires(auth.login() and auth.has_permission('Emp', 'auth_user'))
def employee():
	response.flash = "Welcome to Employee Lgoin"
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
		
	ipa = request.env.remote_addr
	ipaddr = str(ipa[33:])
	import datetime
	import time, os
	os.environ['TZ'] = 'Asia/Kolkata'
	time.tzset()
	currentdate=datetime.date.today()
	now = time.localtime(time.time())
	starttime = datetime.datetime.now()
	session.starttime = starttime
	currenttime = time.strftime("%H:%M:%S", now)
	session.time = currenttime
	if session.cutime == session.time:
		for row in db(db.auth_user.email == auth.user.email).select(db.auth_user.first_name, db.auth_user.employee_code):
			firstname=row.first_name
			empcode=row.employee_code
		db.employee_login_detail.insert(employee_code = empcode, employee_email = auth.user.email, employee_name=firstname, employee_login_date=currentdate, employee_login_time=currenttime, ip_address=ipaddr)
		db.commit()
	else:
		pass
	return dict(algin=algin,images=images)	

@auth.requires_permission('Emp', 'auth_user')	
def emp_mydoc():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)	
	for row in db(db.auth_user.email==auth.user.email).select(db.auth_user.employee_code):
			ecode=row.employee_code
			
	db.document.id.readable=False	
	db.document.email.writable=False
	db.document.email.default=auth.user.email
	db.document.employee_code.writable=False
	db.document.employee_code.default=ecode
	table=SQLFORM.grid(db.document.email==auth.user.email)
	return dict(algin=algin,images=images,table=table)

@auth.requires_permission('Emp', 'auth_user')	
def emp_compliance():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
		
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	return dict(algin=algin,images=images)

@auth.requires_permission('Emp', 'auth_user')	
def emp_all():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	return dict(algin=algin,images=images)

@auth.requires_permission('Emp', 'auth_user')   
def emp_myprofile():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
		
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	for row in db(db.auth_user.email == auth.user.email).select():
		empcode=row.employee_code
		empfname=row.first_name
		emplname=row.last_name
		empemail=auth.user.email 
		emppemail=row.personal_email
		empdoj=row.date_of_joining
		empdpt=row.department
		emprptmgr=row.reporting_manager
		empdgn=row.designation
		
	for row1 in db(db.personal_information.email == auth.user.email).select():
		session.empdob=row1.date_of_birth
		session.empgndr=row1.gender
		session.empstatus=row1.marital_status
		session.empgrp=row1.blood_group
		session.empmbl=row1.mobile
		session.empphone=row1.phone
		session.emppaddr=row1.present_address
		session.empperaddr=row1.permanent_address
		session.empctz=row1.citizenship
		session.empst=row1.state
		session.emppassno=row1.passport_no
		session.empbank=row1.bank_account_no
		session.emppancard=row1.pan_card_no
	edtable = db(db.qualification.email==auth.user.email).select(db.qualification.ALL) 
	return dict(algin=algin,images=images,empcode=empcode,empfname=empfname,emplname=emplname,empemail=empemail,emppemail=emppemail,empdoj=empdoj,empdpt=empdpt,emprptmgr=emprptmgr,empdgn=empdgn,empdob=session.empdob,empgndr=session.empgndr,empstatus=session.empstatus,empgrp=session.empgrp,empmbl=session.empmbl,empphone=session.empphone,emppaddr=session.emppaddr,empperaddr=session.empperaddr,empctz=session.empctz,empst=session.empst,emppassno=session.emppassno,empbank=session.empbank,emppancard=session.emppancard,edtable=edtable)

@auth.requires_permission('Emp', 'auth_user')	
def emp_update_edu_info():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
		
	for row in db(db.auth_user.email==auth.user.email).select(db.auth_user.employee_code):
			ecode=row.employee_code
			
	db.qualification.id.readable=False	
	db.qualification.email.writable=False
	db.qualification.email.default=auth.user.email
	db.qualification.employee_code.writable=False
	db.qualification.employee_code.default=ecode
	table=SQLFORM.grid(db.qualification.email==auth.user.email)
	return dict(algin=algin,images=images,table=table)

@auth.requires_permission('Emp', 'auth_user')
def emp_update_personal_info():
	for row1 in db(db.image.email == auth.user.email).select():
		images=row1.image
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	
	for row in db(db.personal_information.email == auth.user.email).select():
		ecode=row.employee_code
		dbr=row.date_of_birth
		gndr=row.gender
		mstat=row.marital_status
		bgrp=row.blood_group
		mbl=row.mobile
		ph=row.phone
		paddr=row.present_address
		peraddr=row.permanent_address
		ctz=row.citizenship
		st=row.state
		pno=row.passport_no
		bno=row.bank_account_no
		pcard=row.pan_card_no		
		
	db.personal_information.email.writable=False
	db.personal_information.employee_code.writable=False
	db.personal_information.email.default=auth.user.email
	db.personal_information.employee_code.default=ecode
	
	db.personal_information.date_of_birth.default=dbr 
	db.personal_information.gender.default=gndr
	db.personal_information.marital_status.default=mstat
	db.personal_information.blood_group.default=bgrp
	db.personal_information.mobile.default=mbl
	db.personal_information.phone.default=ph
	db.personal_information.present_address.default=paddr 
	db.personal_information.permanent_address.default=peraddr
	db.personal_information.citizenship.default=ctz
	db.personal_information.state.default=st
	db.personal_information.passport_no.default=pno
	db.personal_information.bank_account_no.default=bno
	db.personal_information.pan_card_no.default=pcard 
	
	form = SQLFORM(db.personal_information)
	if form.accepts(request.vars, session):
		dob = form.vars.date_of_birth
		gndr = form.vars.gender
		mstatus = form.vars.marital_status
		bgrp = form.vars.blood_group
		mbl = form.vars.mobile
		phone = form.vars.phone
		paddr = form.vars.present_address
		peraddr = form.vars.permanent_address
		ctz = form.vars.citizenship
		st = form.vars.state
		pno = form.vars.passport_no
		baccno = form.vars.bank_account_no
		pcard = form.vars.pan_card_no
		img = form.vars.image
		db(db.personal_information.email == auth.user.email).update(date_of_birth=dob, gender=gndr, marital_status=mstatus, blood_group=bgrp, mobile=mbl, phone=phone, present_address=paddr, permanent_address=peraddr, citizenship=ctz, state=st, passport_no=pno, bank_account_no=baccno, pan_card_no=pcard)
		redirect(URL(c='default', f='emp_myprofile'))
	return dict(algin=algin,form=form,images=images)

@auth.requires_permission('Emp', 'auth_user')
def emp_update_image():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
		
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	for row1 in db(db.image.email == auth.user.email).select():
		mail=row.email
		ecode=row.employee_code
		
	db.image.email.writable=False
	db.image.employee_code.writable=db.image.employee_code.readable=False
	db.image.email.default=mail
	form=SQLFORM(db.image)
	if form.accepts(request.vars, session):
		img = form.vars.image
		db(db.image.email == auth.user.email).update(image=img)
		redirect(URL(c='default', f='emp_myprofile'))
	return dict(algin=algin,images=images,form=form)

@auth.requires_permission('Emp', 'auth_user')
def emp_company():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
		
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	return dict(algin=algin,images=images)

@auth.requires_permission('Emp', 'auth_user')	
def emp_organization():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	return dict(algin=algin,images=images)

@auth.requires_permission('Emp', 'auth_user')	
def emp_leavecalendar():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	totvacationleave=18
	totmedicalleave=6
	totcasualleave=6
	empleave = db(db.employee_leave.email==auth.user.email).select(db.employee_leave.ALL)
	empstat = db(db.apply_leave.email==auth.user.email).select(db.apply_leave.ALL)
	return dict(algin=algin,empstat=empstat,images=images,empleave=empleave,totvacationleave=totvacationleave,totmedicalleave=totmedicalleave,totcasualleave=totcasualleave)
	
def cron_leave():
	totvacationleave=18
	totmedicalleave=6
	totcasualleave=6
	tvl=0
	tml=0
	tcl=0
	for row in db(db.employee_leave.id>0).select():
		for row1 in db(db.employee_leave.id==row.id).select():
			totvacleave = totvacationleave + row1.left_vacation_leave
			db(db.employee_leave.id==row.id).update(taken_vacation_leave=tvl, taken_medical_leave=tml, taken_casual_leave=tcl, left_vacation_leave=totvacleave, left_medical_leave=totmedicalleave, left_casual_leave=totcasualleave)
			db.commit()
	return ''	
	
@auth.requires_permission('Emp', 'auth_user')	
def emp_calendar():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
		
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	caland=db().select(db.holiday_list.ALL)
	return dict(algin=algin,images=images,rows=caland)

@auth.requires_permission('Emp', 'auth_user')	
def emp_calread():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	record = db.holiday_list(request.args(0)) or redirect(URL('error'))
	form=crud.read(db.holiday_list,record)
	return dict(form=form,images=images,algin=algin)
    
@auth.requires_permission('Emp', 'auth_user')	
def emp_apply_leave():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	for row in db(db.auth_user.email==auth.user.email).select():
		rptmgr=row.reporting_manager
	return dict(algin=algin,images=images)

@auth.requires_permission('Emp', 'auth_user')	
def submit_emp_apply_leave():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
		
	import datetime
	session.fromdate=request.vars.fromleave
	session.todate=request.vars.toleave
	fdate=datetime.date(*map(int, session.fromdate.split('-')))
	tdate=datetime.date(*map(int, session.todate.split('-')))
	totday=tdate-fdate
	session.day=totday.days
	if request.vars.apply == 'Casual Leave':
		for row in db(db.employee_leave.email==auth.user.email).select():
			if session.day <= row.left_casual_leave:
				for row in db(db.auth_user.email==auth.user.email).select():
					session.rptmgr=row.reporting_manager
					session.empcode=row.employee_code
					session.fname=row.first_name
				db.apply_leave.insert(employee_code=session.empcode,email=auth.user.email,name=session.fname,leave_type=request.vars.apply,from_leave=session.fromdate,to_leave=session.todate,total_day=session.day,reason_for_leave=request.vars.reason,reporting_manager=session.rptmgr)
				db.commit()
				leavemail()
			else:
				response.flash='Your Casual leave is not left'
	elif request.vars.apply == 'Medical Leave':
		for row in db(db.employee_leave.email==auth.user.email).select():
			if session.day <= row.left_medical_leave:
				for row in db(db.auth_user.email==auth.user.email).select():
					session.rptmgr=row.reporting_manager
					session.empcode=row.employee_code
					session.fname=row.first_name
				db.apply_leave.insert(employee_code=session.empcode,email=auth.user.email,name=session.fname,leave_type=request.vars.apply,from_leave=session.fromdate,to_leave=session.todate,total_day=session.day,reason_for_leave=request.vars.reason,reporting_manager=session.rptmgr)
				db.commit()
				leavemail()
			else:
				response.flash='Your Medical leave is not left'
	elif request.vars.apply == 'Vacation Leave':
		for row in db(db.employee_leave.email==auth.user.email).select():
			if session.day <= row.left_vacation_leave:
				for row in db(db.auth_user.email==auth.user.email).select():
					session.rptmgr=row.reporting_manager
					session.empcode=row.employee_code
					session.fname=row.first_name
				db.apply_leave.insert(employee_code=session.empcode,email=auth.user.email,name=session.fname,leave_type=request.vars.apply,from_leave=session.fromdate,to_leave=session.todate,total_day=session.day,reason_for_leave=request.vars.reason,reporting_manager=session.rptmgr)
				db.commit()
				leavemail()
			else:
				response.flash='Your Vacation leave is not left'
	else:
		pass	
	return dict(algin=algin,images=images)	

@auth.requires_permission('Emp', 'auth_user')	
def leavemail():
    from gluon.tools import Mail
    mail=Mail()
    #specify server
    
    mail=auth.settings.mailer
    mail.settings.server='smtp.gmail.com:587'
    mail.settings.login='themisdemo1@gmail.com:123456asdfg'
    #specify address to send as
    mail.settings.sender='themisdemo1@gmail.com'
    #send the message                             
    mail.send(to=[session.rptmgr],
            subject='Request for Leave',
            message='<html>'
                        '<body>'
                            '<span style="font-family: Bodoni MT Ultra Bold;color:  #000000 ;font-size : 18pt;"><b>Themis </span></h1><span style="font-family: Bodoni MT Ultra Bold;color:#C7A317   ;font-size :18pt;"><b>Lexsol</b></span>'
                            
                            '<p>Dear &nbsp;'+session.fname+' applied for leave</p>'
                            '<p>Emp Code &nbsp;'+session.empcode+' </p>'
                             '<p>From Date &nbsp;'+session.fromdate+' </p>'
                              '<p>To Date &nbsp;'+session.todate+' </p>'
                               '<p>Total Day &nbsp;'+str(session.day)+' </p>'
                            
                            '<p></p>'
                            '<center><p>_________________________________________________________</p><p style="color:red;font-size :5pt;">This email comes to you since your company has subcribed for LCM Plus. TO unsubcribed please contact to Themis Lexsol</p></center>'
                      
                        '</body>'
                    '</html>'
                    
  )
    response.flash='mail send'
    redirect(URL(c='default',f='emp_leavecalendar'))
    return ''	

	
@auth.requires_permission('Mgr', 'auth_user')	
def emp_leave_stat():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
		
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	empleave=db(db.apply_leave.reporting_manager==auth.user.email).select(db.apply_leave.ALL)
	return dict(algin=algin,images=images,empleave=empleave)
	
@auth.requires_permission('Mgr', 'auth_user')		
def emp_edit_leave():
	for row in db(db.image.email == auth.user.email).select():
		images=row.image
		
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	for row in db(db.apply_leave.id==request.args(0)).select():
		id=row.id
		eid=row.employee_code
		estat=row.status
		eltype=row.leave_type
		efrom=row.from_leave
		eto=row.to_leave
		ereason=row.reason_for_leave
		etotday=row.total_day
	return dict(algin=algin,id=id,images=images,eid=eid,estat=estat,eltype=eltype,efrom=efrom,eto=eto,ereason=ereason,etotday=etotday)
	
@auth.requires_permission('Mgr', 'auth_user')		
def emp_approve_leave():
	for row in db(db.apply_leave.id==request.args(0)).select():
		session.elmail=row.email
		session.eempname=row.name
		session.eefrom=row.from_leave
		session.eeto=row.to_leave
		session.estatus=request.vars.status
		session.eltype=row.leave_type
		session.etday=row.total_day
	if session.estatus == 'Approved':
		if session.eltype == 'Casual Leave':
			for row in db(db.employee_leave.email==session.elmail).select():
				totday=row.left_casual_leave - session.etday
			db(db.apply_leave.id==request.args(0)).update(status=session.estatus, approved_by='Reporting Manager')
			db(db.employee_leave.email==session.elmail).update(taken_casual_leave=session.etday,left_casual_leave=totday)
			db.commit()
			redirect(URL(c='default', f='emp_leave_mail'))
		elif session.eltype == 'Medical Leave':
			for row in db(db.employee_leave.email==session.elmail).select():
				totday=row.left_medical_leave - session.etday
			db(db.apply_leave.id==request.args(0)).update(status=session.estatus, approved_by='Reporting Manager')
			db(db.employee_leave.email==session.elmail).update(taken_medical_leave=session.etday,left_medical_leave=totday)
			db.commit()
			redirect(URL(c='default', f='emp_leave_mail'))
		elif session.eltype == 'Vacation Leave':
			for row in db(db.employee_leave.email==session.elmail).select():
				totday=row.left_vacation_leave - session.etday
			db(db.apply_leave.id==request.args(0)).update(status=session.estatus, approved_by='Reporting Manager')
			db(db.employee_leave.email==session.elmail).update(taken_vacation_leave=session.etday,left_vacation_leave=totday)
			db.commit()
			redirect(URL(c='default', f='emp_leave_mail'))
		else:
			pass
	else:
		db(db.apply_leave.id==request.args(0)).update(status=session.estatus, approved_by='Reporting Manager')
		db.commit()
		redirect(URL(c='default', f='emp_leave_mail'))
	return ''
	
@auth.requires_permission('Mgr', 'auth_user')	
def emp_leave_mail():
    from gluon.tools import Mail
    mail=Mail()
    #specify server
    mail=auth.settings.mailer
    mail.settings.server='smtp.gmail.com:587'
    mail.settings.login='themisdemo1@gmail.com:123456asdfg'
    #specify address to send as
    mail.settings.sender='themisdemo1@gmail.com'
    #send the message                             
    mail.send(to=[session.elmail],
            subject='Leave Status',
            message='<html>'
                        '<body>'
                            '<span style="font-family: Bodoni MT Ultra Bold;color:  #000000 ;font-size : 18pt;"><b>Themis </span></h1><span style="font-family: Bodoni MT Ultra Bold;color:#C7A317   ;font-size :18pt;"><b>Lexsol</b></span>'
                            
                            '<p>Dear &nbsp;'+session.eempname+'</p>'
                            
                            '<p>I just wanted to drop you a quick message to say Your leave request from '+str(session.eefrom)+' to '+str(session.eeto)+' is '+session.estatus+' If you need help at any time, please contact me by replying to this message. Similarly, if you ever have any questions then please do not hesitate to send me a message or email.</p>'
                            '<center><p>_________________________________________________________</p><p style="color:red;font-size :5pt;">This email comes to you since you are subcribed for HRMS. TO unsubcribed please contact to Themis Lexsol</p></center>'
                      
                        '</body>'
                    '</html>'
                    
  )
    redirect(URL(c='default', f='emp_cnf_leave'))	
    return ''
    
@auth.requires_permission('Mgr', 'auth_user')	
def emp_cnf_leave():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
		
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	return dict(algin=algin,images=images,status=session.estatus,efrom=session.eefrom,eto=session.eeto,empname=session.eempname)
	
@auth.requires_permission('Mgr', 'auth_user')
def emp_edit_leave_status():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
		
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	ltype=['Casual Leave','Medical Leave','Vacation Leave']
	session.eeleaveid=request.args(0)
	for row in db(db.apply_leave.id==session.eeleaveid).select():
		ecode=row.employee_code
		name=row.name
		fle=row.from_leave
		tle=row.to_leave
		tday=row.total_day
		rle=row.reason_for_leave
		eltype=row.leave_type
	return dict(algin=algin,ltype=ltype,images=images,ecode=ecode,name=name,fle=fle,tle=tle,tday=tday,rle=rle,eltype=eltype)

@auth.requires_permission('Mgr', 'auth_user')	
def emp_submit_edit_leave_status():
	db(db.apply_leave.id == session.eeleaveid).update(name=request.vars.name, leave_type=request.vars.ltype, from_leave=request.vars.fleave, to_leave=request.vars.tleave, total_day=request.vars.tday, reason_for_leave=request.vars.rleave)
	db.commit()
	redirect(URL(c='default',f='emp_leave_stat'))
	return ''

@auth.requires_permission('Emp', 'auth_user')
def user_timesheet():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
		
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	proj=db(db.assign_project.employee==auth.user.email).select(db.project.ALL)
	if request.vars.activitysubmit:
		var = 'The Activity for Project ('+request.vars.activitysubmit+') is submitted Successfully. Please Select Project to continue your work.'
	else:
		var='Time Sheet'
	return dict(images=images,algin=algin,proj=proj,var=var)	

@auth.requires_permission('Emp', 'auth_user')	
def emp_task():
	tsk=[]
	for row in db(db.activity.id == request.vars.pro).select():
		tsk.append(row.activity)
	return SELECT(_id="tsk",_name="tsk",*[OPTION((act), _value=str (act)) for act in tsk])

@auth.requires_permission('Emp', 'auth_user')	
def emp_task_timesheet():
	for row in db(db.project.id == request.vars.pro).select():
		proj=row.project_name
	projtask=request.vars.tsk
	return TABLE([TR("Project:",INPUT(_type="text",id="txt1",_name="proname",_value=proj,_readonly="readonly")),TR("Task:",INPUT(_type="text",_id="txt2",_name="protask",_value=projtask)),TR("Time:",INPUT(_type="text",_id="txt",_name="protime",_value=""))])

@auth.requires_permission('Emp', 'auth_user')	
def adata():
	import datetime
	dte=datetime.date.today()
	pro=request.vars.proname
	for row1 in db(db.project.project_name==pro).select():
		client=row1.client_name
		for row2 in db(db.auth_user.id==row1.project_manager).select():
			promgr=row2.email
	ptask=request.vars.protask
	ptime=request.vars.protime
	for row in db(db.auth_user.email==auth.user.email).select():
		rmgr=row.reporting_manager
	return TABLE([TR("Project Name:",INPUT(_type="text",_name="proj",_value=pro,_readonly="readonly")),TR("Client Name:",INPUT(_type="text",_name="client",_value=client,_readonly="readonly")),TR("Reporting Manager:",INPUT(_type="text",_name="rpm",_value=rmgr,_readonly="readonly")),TR("Project Manager:",INPUT(_type="text",_name="pmr",_value=promgr,_readonly="readonly")),TR("Project Task:",INPUT(_type="text",_name="protsk",_value=ptask,_readonly="readonly")),TR("Date:",INPUT(_type="text",_name="dte",_value=dte,_readonly="readonly")),TR("Task Discription:",INPUT(_type="text",_name="tskdisc",_value="")),TR("Total Time:",INPUT(_type="text",_name="tottme",_value=ptime))])
	
@auth.requires_permission('Emp', 'auth_user')
def emp_submit_timesheet():
	for row1 in db(db.project.project_name==request.vars.proj).select():
		session.cmpnytime=row1.company_name
		session.cmpnyemailtime=row1.company_email
	for row in db(db.auth_user.email==auth.user.email).select():
		ecode=row.employee_code
	db.activity_tracker.insert(employee_code=ecode,email=auth.user.email,project_name=request.vars.proj,project_task=request.vars.protsk,task_description=request.vars.tskdisc,date=request.vars.dte,total_time=request.vars.tottme,client_name=request.vars.client,company_name=session.cmpnytime,company_email=session.cmpnyemailtime,practice_head=request.vars.rpm,project_manager=request.vars.pmr)
	db.commit()
	redirect(URL(c='default', f='user_timesheet', vars={'activitysubmit':request.vars.proj}))
	return dict()

@auth.requires_permission('Mgr', 'auth_user')	
def emp_activity():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	db.activity.id.readable = False
	form=SQLFORM.grid(db.activity,selectable = lambda ids: emp_del_activity(ids))
	return dict(images=images,form=form,algin=algin)
	
@auth.requires_permission('Mgr', 'auth_user')	
def emp_del_activity(ids):
	if not ids:
		response.flash='Please Select the Check-box to Delete'
	else:
		for row in ids:
			db(db.activity.id == row).delete()
		pass
	pass
	return ''
	
@auth.requires_permission('Mgr', 'auth_user')	
def emp_assign_project():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	db.assign_project.id.readable=False
	form=SQLFORM.grid(db.assign_project,create=False,selectable = lambda ids: del_emp_assign_project(ids))
	return dict(images=images,form=form,algin=algin)

@auth.requires_permission('Mgr', 'auth_user')	
def del_emp_assign_project(ids):
	if not ids:
		response.flash='Please Select the Check-box to Delete'
	else:
		for row in ids:
			db(db.assign_project.id == row).delete()
		pass
	pass
	return ''
	
@auth.requires_permission('Mgr', 'auth_user')	
def emp_assign_pro():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
	proj=db().select(db.project.ALL)
	orzn=db().select(db.add_new_organization.ALL)
	dept=db().select(db.add_new_department.ALL)
	llgin=[]
	for log in db(db.employee_login_detail.employee_logout_date=='Logged in').select():
		llgin.append(log.employee_name)
	blgin=set(llgin)
	algin=list(blgin)
	return dict(images=images,proj=proj,orzn=orzn,dept=dept,algin=algin)
	
@auth.requires_permission('Mgr', 'auth_user')	
def emp_orz():
	for row in db(db.add_new_organization.id == request.vars.orz).select():
		organization=row.organization_name
	for row1 in db(db.add_new_department.id == request.vars.dp).select():
		department=row1.department
	
	usr=[]
	for row in db((db.auth_user.department == department) & (db.auth_user.organization_name == organization)).select():
		usr.append(row.email)
	return SELECT(_id="usr",_name="usr",*[OPTION((emp), _value=str (emp)) for emp in usr])
	
@auth.requires_permission('Mgr', 'auth_user')	
def emp_submit_assign_project():
	for row2 in db(db.image.email == auth.user.email).select():
		images=row2.image
	for row in db(db.add_new_organization.id == request.vars.orz).select():
		organization=row.organization_name
	for row1 in db(db.add_new_department.id == request.vars.dp).select():
		department=row1.department
	db.assign_project.insert(project_name=request.vars.pro,organization_name=organization,department=department,employee=request.vars.usr)
	db.commit()
	redirect(URL(c='default',f='emp_assign_project'))
	return dict(images=images)
