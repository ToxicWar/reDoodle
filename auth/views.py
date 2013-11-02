#coding: utf-8
from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import Http404, HttpResponse
from django.conf import settings
from django.views.generic.edit import FormView
#from django.forms import ValidationError
from django.core import validators
from django.core.mail import send_mail
from django.core.urlresolvers import reverse, reverse_lazy
from .forms import LoginForm, RegistrationForm, EmailForm
from random import randint
from hashlib import md5
import json


# json.dumps(data)
def login_view(request):
	if request.method != 'POST':
		raise Http404
	
	form = LoginForm(request.POST)
	if form.is_valid():
		auth_login(request, form.user)
		return HttpResponse('', content_type="application/json", status=200)
	
	return HttpResponse('{"errors": '+json.dumps(form._errors)+'}',
		content_type="application/json", status=400)


def logout(request):
	auth_logout(request)
	return HttpResponse(content_type="application/json", status=200)


def register_view(request):
	if request.method != 'POST':
		raise Http404
	
	form = RegistrationForm(request.POST)
	if form.is_valid():
		form.save()
		# коли дали мыло, проверяем сразу
		if form.cleaned_data['email']: # 'email' in form.cleaned_data
			mail_confirm_send(form.user,
			                  form.cleaned_data['email'],
			                  request.META['HTTP_HOST'])
		return HttpResponse(content_type="application/json", status=200)
	
	return HttpResponse('{"errors": '+json.dumps(form._errors)+'}',
		content_type="application/json", status=400)


#TODO: do something with HttpResponse'es
#TODO: mb use render_to_string(file, context)
#mail server: python -m smtpd -n -c DebuggingServer localhost:1025
#steps:
# * POST - get email (if any), send code to email
# * GET  - get code, compare, activate
#confirmation code is stored in user's first name
#new email is stored in user's last name
def mail_confirm_send(user, email, site_host):
	code = md5(str(randint(0,65536) + user.id)).hexdigest()[:-2] # потому что 32 и не влезает
	url = "http://"+site_host+reverse("mail_confirm")
	user.first_name = code
	user.last_name = email
	send_mail("Wanna enlarge your... permissions?",
	          "Message, "+url+"?code="+code,
	          settings.EMAIL_HOST_USER, [email])
	user.save()
	print code, user.first_name

@login_required
def mail_confirm_view(request):
	user = request.user
	#(1) mail sending phase
	if request.POST:
		#saving email
		form = EmailForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			#sending code
			mail_confirm_send(user, email, request.META['HTTP_HOST'])
			user.save()
			return HttpResponse("Code was sended. Check e-mail.")
	#(2) mail confirmation phase
	else:
		if 'code' in request.GET and request.GET['code'] == user.first_name:
			user.is_active = True
			user.email = user.last_name
			user.first_name = user.last_name = ''
			user.save()
			return HttpResponse("Activation complete!")
		else:
			init = {'email': user.email} if user.email else {}
			form = EmailForm(initial=init)
	
	return TemplateResponse(request, "mail_confirm.html", {'form': form})


#"""unused down there"""

#validator = {
#	'name':     [r'^.{3,}$', u'Wrong name (3-128 symbols)'],
#	'mail':     [r'^[\w]{1,128}@[\w]{1,64}\.[\w]{1,8}$', u'Wrong e-mail'],
#	'password': [r'^.{5,128}$', u'Wrong password (5-128 symbols)']
#}

#for k, v in validator.iteritems():
#	validator[k][0] = RegexValidator(regex=re.compile(v[0]))


#def validate(post):
#	info = {}
#	for k, v in validator.iteritems():
#		v = validator[k]
#		try:
#			v[0](post[k])
#		except ValidationError:
#			info[k] = v[1]
#	return info

