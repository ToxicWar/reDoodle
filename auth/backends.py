from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class LoginBackend(ModelBackend):
	
	def authenticate(self, username=None, password=None, error_info=[]):
		if not username or not password:
			return None
		
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			error_info.append('name')
			return None
		
		if not user.check_password(password):
			error_info.append('pass')
			return None
		
		return user


class VKLoginBackend(ModelBackend):
	
	def authenticate(self, email=None):
		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			return None
		
		return user
