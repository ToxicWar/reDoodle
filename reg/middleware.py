# coding: utf-8

from forms import LoginForm, RegistrationForm
#from backends.default import DefaultBackend
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
#from django.conf import settings
from django.contrib.auth import login
from django.http import HttpResponse


class LoginMiddleware(object):
	def process_request(self, request):
		print "login", request.POST
		
		if request.POST and 'login_form_mark' in request.POST:
			#if it is POST and it is LOGIN POST
			print "login POST"
			form = LoginForm(data=request.POST)
			
			if form.is_valid():
				user = form.user
				login(request, user)
				print "login USER",user,"LOGGED IN"
				
				#login() must have set test cookie
				if request.session.test_cookie_worked():
					request.session.delete_test_cookie()
				else:
					#TODO: do it in more accurate way
					return HttpResponse("Enable cookies plz, they r yummy.")
				
				#in contrib/auth/views.py redirect_to is
				#a bit more complex. mb worth using.
				# * it is for redirection path checking
				
				return redirect(
					reverse('index') if request.path == reverse('login')
					else request.path)
				
			else:
				# not valid
				if request.path == reverse('login'):
					# if we are on login page, refresh it
					print "login refresh"
					request.login_form = form
					return TemplateResponse(request, 'login.html')
				else:
					# if not on login page, redirect to it
					print "login not valid not on login page"
					request.session['login_form'] = form
					return redirect('login')
			
		else:
			# if not post, pop saved form (if any) and pass it further
			print "login no POST"
			if 'login_form' in request.session:
				print "login restore form from session"
				form = request.session['login_form']
				del request.session['login_form']
			else:
				print "login no form in session"
				form = LoginForm()
		
		print "login in request",request.user if 'user' in request else "no user"
		request.session.set_test_cookie()
		request.login_form = form


class RegistrationMiddleware(object):
	def process_request(self, request):
		
		if request.POST and 'reg_form_mark' in request.POST:
			#if  POST has commen and mark was found, it's a registration attempt
			print "reg POST"
			
			form = RegistrationForm(data=request.POST)
			if form.is_valid():  # valid - create user
				form.save()  # creates User object and saves it
				return TemplateResponse(request, "reg_complete.html")
			else:
				# if not valid on reg page, just refresh it
				if request.path == reverse('register'):
					request.reg_form = form
					return TemplateResponse(request, 'register.html')
				else:  # if not on reg page, redirect to it
					request.session['reg_form'] = form
					return redirect('register')
			
		else:
			# if it's not POST, prepare form
			if 'reg_form' in request.session:
				# form found in backup => was redirected here
				print "reg not POST, found form"
				form = request.session['reg_form']
				del request.session['reg_form']
			else:
				# no form in backup => page just has been opened
				print "reg not POST, no form"
				form = RegistrationForm()
		
		request.reg_form = form

