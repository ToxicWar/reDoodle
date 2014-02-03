from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User


class LoginBackend(ModelBackend):
	
	def authenticate(self, username, password, error_info):
		try:
			user = User.objects.get(username = username)
		except User.DoesNotExist:
			error_info.append('name')
			return None
		
		if not user.check_password(password):
			error_info.append('pass')
			return None
		
		return user
