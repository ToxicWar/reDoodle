# coding: utf-8

from django import forms
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.contrib.auth.backends import ModelBackend


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())
	login_form_mark = forms.CharField(widget=forms.HiddenInput(),
	                                  required=False, label="")
	
	#def __init__(self, *args, **kwargs):
	#	super(LoginForm, self).__init__(*args, **kwargs)
	def clean(self):
		if self._errors:
			return self.cleaned_data
		
		data = self.cleaned_data
		try:
			user = User.objects.get(username=data['username'])
			print "searching for " + data['username']
			if user.check_password(data['password']):
				#some holy stuff is happening during user login
				#backend must be passed
				user.backend = 'django.contrib.auth.backends.ModelBackend'
				self.user = user
				print "user",user
			else:
				print "wrong pass"
				self._errors['password'] = ErrorList(["Wrong user's password"])
		except User.DoesNotExist:
			print "no such user"
			self._errors['username'] = ErrorList(["No such user"])
		
		return data


class RegistrationForm(forms.Form):
	username = forms.CharField()
	email = forms.EmailField()
	password = forms.CharField(widget=forms.PasswordInput())
	reg_form_mark = forms.CharField(widget=forms.HiddenInput(),
	                                required=False, label="")
	
	def clean(self):
		if self._errors:
			return self.cleaned_data
		
		data = self.cleaned_data
		try:
			user = User.objects.get(username=data['username'])
			self._errors['username'] = ErrorList(["User already exists"])
		except User.DoesNotExist:
			pass
		return data
	
	def save(self):
		data = self.cleaned_data
		user = User.objects.create_user(data['username'],
		                                data['email'], data['password'])
		user.is_active = False
		user.save()

