# coding: utf-8

from django import forms
from django.contrib.auth.models import User
from django.forms.util import ErrorList
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import authenticate


class LoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget=forms.PasswordInput())
	
#	def __init__(self, *args, **kwargs):
#		super(LoginForm, self).__init__(*args, **kwargs)
	
	def clean(self):
		if self._errors:
			return self.cleaned_data
		
		data = self.cleaned_data
		username = data['username']
		password = data['password']
		
		err_info = []
		user = authenticate(username=username, password=password,
		                    error_info=err_info)
		if user is None:
			if err_info[0] == "name":
				self._errors['username'] = ErrorList([u'А нет такого пользователя'])
			elif err_info[0] == "pass":
				self._errors['password'] = ErrorList([u'Кто-то ошибся в пароле'])
		else:
			self.user = user
		
		return data


class RegistrationForm(forms.Form):
	username = forms.CharField()
	email = forms.EmailField(required=False)
	password = forms.CharField(widget=forms.PasswordInput())
	
	def clean(self):
		if self._errors:
			return self.cleaned_data
		
		data = self.cleaned_data
		
		try:
			user = User.objects.get(username=data['username'])
			self._errors['username'] = ErrorList([u'Имя занято'])
		except User.DoesNotExist:
			pass
		
		try:
			user = User.objects.get(email=data['email'])
			self._errors['email'] = ErrorList([u'Почта занята'])
		except User.DoesNotExist:
			pass
		
		return data
	
	def save(self):
		data = self.cleaned_data
		user = User.objects.create_user(data['username'],
		                                data['email'], data['password'])
		user.is_active = False
		user.save()
		self.user = user # надо вьюхе для отправки почты


class EmailForm(forms.Form):
	email = forms.EmailField()

