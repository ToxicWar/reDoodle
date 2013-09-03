from django.template.response import TemplateResponse
from django.template.loader import render_to_string
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import Http404, HttpResponse
from django.conf import settings
from django.views.generic.edit import FormView
from django.forms import ValidationError
from django.core import validators
from django.core.urlresolvers import reverse, reverse_lazy
from .forms import LoginForm, RegistrationForm


class LoginView(FormView):
	template_name = "login.html"
	form_class = LoginForm
	
	def get_success_url(self):
		if 'next' in self.request.GET:
			return self.request.GET['next']
		return reverse("index")
	
	def form_valid(self, form):
		data = form.cleaned_data
		auth_login(self.request, form.user)
		return super(LoginView, self).form_valid(form)


def logout(request):
	auth_logout(request)
	return redirect('index')

class RegisterView(FormView):
	template_name = "register.html"
	form_class = RegistrationForm
	success_url = reverse_lazy("index")
	
	def form_valid(self, form):
		form.save()
		return super(RegisterView, self).form_valid(form)


#TODO: do something with HttpResponse'es
#TODO: mb use render_to_string(file, context)
#mail server: python -m smtpd -n -c DebuggingServer localhost:1025
#steps:
# * POST - get email (if any), send code to email
# * GET  - get code, compare, activate
#confirmation code is stored in user's first name
@login_required
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
			code = str(12345 + user.id)  #TODO: normal generation
			user.first_name = code
			user.save()
			user.email_user(
				"Wanna enlarge your... permissions?",
				"Message, http://"+request.META['HTTP_HOST']+reverse("mail_confirm")+"?code="+code,
				settings.DEFAULT_FROM_EMAIL)
			return HttpResponse("Code was sended. Check e-mail.")
	#(2) mail confirmation phase
	elif request.GET:
		if 'code' in request.GET and request.GET['code'] == user.first_name:
			user.is_active = True
			user.first_name = ''
			user.save()
			return HttpResponse("Activation complete!")
	
	raise Http404


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

