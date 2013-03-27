from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.contrib.auth import logout as auth_logout
from django.shortcuts import redirect
from django.http import Http404, HttpResponse
from django.conf import settings
from django.core import validators


#TODO: move this to middleware
def login(request):
	return TemplateResponse(request, "login.html")

def logout(request):
	auth_logout(request)
	return redirect('index')

def register(request):
	return TemplateResponse(request, "register.html")


#TODO: do something with HttpResponse'es
#TODO: mb use render_to_string(file, context)
#mail server: python -m smtpd -n -c DebuggingServer localhost:1025
#steps:
# * POST - get email (if any), send code to email
# * GET  - get code, compare, activate
#confirmation code is stored in user's first name
def mail_confirm_send(user):
	code = str(12345 + user.id)  #TODO: normal generation
	user.first_name = code
	user.email_user("Wanna enlarge your... permissions?", "Message, code: "+code, settings.DEFAULT_FROM_EMAIL)

def mail_confirm_view(request):
	user = request.user
	#(1) mail sending phase
	if request.POST:
		#saving email
		if 'email' in request.POST:
			email = request.POST['email']
			try:
				validators.validate_email(email)
			except ValidationError, e:
				#TODO: do it NORMAL way (mb params to context, mb use messages)
				return HttpResponse(e.messages[0])
			user.email = email
		
		#sending code
		if user.email:
			mail_confirm_send(user)
			user.save()
			return HttpResponse("Code was sended. Check e-mail.")
	#(2) mail confirmation phase
	elif request.GET and 'code' in request.GET:
		if request.GET['code'] == user.first_name:
			user.is_active = True
			user.first_name = ''
			user.save()
			return HttpResponse("Activation complete!")
	
	raise Http404



#from django.template.response import TemplateResponse
#from django.core.context_processors import csrf
#from models import User
#from django import forms
#from django.core.validators import validate_email, RegexValidator, ValidationError
#import re
#from django.shortcuts import redirect
#from django.utils.translation import ugettext_lazy as _
#from django.forms.util import ErrorList
#from django.http import Http404
##from django.db.models import Q  # for complex queries

## questions:
## 1) SSL (full/only forms's POST)
## 2) login user search: in form or function? and ok to pass it througt cleaned_data?


#class RegForm(forms.ModelForm):
#	#forms.PasswordInput(render_value=False)
#	password = forms.CharField(label=_("Pass"), widget=forms.PasswordInput, min_length=5, max_length=255)
#	password2 = forms.CharField(label=_("Moar pass"), widget=forms.PasswordInput, min_length=5, max_length=255)

#	class Meta:
#		model = User
#		fields = ('name', 'mail')

#	def clean(self):
#		data = self.cleaned_data
#		err = self._errors
#		if 'name' not in err:
#			if User.objects.filter(name=data['name']):
#				err['name'] = ErrorList(["Name occupied"])
#		if 'mail' not in err:
#			if User.objects.filter(name=data['mail']):
#				err['mail'] = ErrorList(["This mail already used"])
#		if 'password' not in err and 'password2' not in err:
#			if data['password'] != data['password2']:
#				err['password'] = ErrorList(["Passwords must be equal"])
#		return data

#	def save(self, *args, **kwargs):
#		self.instance.new_pass2hash(self.cleaned_data['password'])
#		return super(RegForm, self).save(*args, **kwargs)


#def index(request):
#	if request.method == 'GET':
#		form = RegForm()
#	elif request.method == 'POST':
#		form = RegForm(request.POST)
#		if form.is_valid():
#			request.session['user'] = form.save()
#	else:
#		raise Http404
#	return TemplateResponse(request, 'index.html', {'form': form})


#class LoginForm(forms.ModelForm):
#	password = forms.CharField(label=_("Pass"), widget=forms.PasswordInput, min_length=5, max_length=255)

#	class Meta:
#		model = User
#		fields = ('name',)

#	def clean(self):
#		data = self.cleaned_data

#		if len(self._errors) > 0:
#			return data

#		try:
#			user = User.objects.get(name=self.data['name'])
#			print "searching for " + self.data['name']
#			if user.check_pass(data['password']):
#				data['user'] = user
#				print user
#				print "user"
#			else:
#				print "wrong pass"
#				self._errors['password'] = ErrorList(["Wrong user's password"])
#		except User.DoesNotExist:
#			print "no such user"
#			self._errors['name'] = ErrorList(["No such user"])

#		return data


#def login(request):
#	if request.method == 'GET':
#		form = LoginForm()
#	elif request.method == 'POST':
#		post = request.POST
#		form = LoginForm(post)
#		if form.is_valid():
#			request.session['user'] = form.cleaned_data['user']
#	else:
#		raise Http404
#	return TemplateResponse(request, 'login.html', {'form': form})


#def logout(request):
#	del request.session['user']
#	return redirect('/')


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

