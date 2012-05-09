# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = ' '.join(word.capitalize() for word in request.application.split('_'))
response.subtitle = T('customize me!')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'
response.meta.copyright = 'Copyright 2011'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('HOME'), False, URL('default','index'), [])
    ]
response.menu+=[
	(T('ABOUT US '), False, URL('default','tlsabout'), []),
	(T('OUR EXPERTISE  '), False, URL('default','tlsservice'), []),
	(T('OUR TEAM'), False, URL('default','tlsoteam'), []),
	(T('OPERATIONS'), False, URL('default','tlsoo'), []),
    (T('JOIN US'), False, URL('default','tlscareer'), []),
    (T('CONTACT US'), False, URL('default','tlscontact'), []),
    ]

response.tlsmenu = [
    (T('Website'), False, URL('default','index'), []),
    ]
response.tlsmenu+=[
	 (T('WebMail'), False, URL('default','webmail'), []),
    (T('Themis Portal'), False, URL('default','portal'), []),
    (T('Themis Policies'), False, URL('default','ourtrem'), []),
    (T('Contact Details'), False, URL('default','emp_contact_detail'), []),
    ]
	
response.atlsmenu = [
	 (T('Website'), False, URL('default','index'), []),
    ]
response.atlsmenu+=[
		(T('Webmail'), False, URL('default','#'), []),
	(T('Themis Portal'), False, URL('default','#'), []),
	(T('Themis Policies'), False, URL('default','add_project'), []),
	(T('Contact Details'), False, URL('default','admin_contact_detail'), []),
    ]
#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources

