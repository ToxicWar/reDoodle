# coding: utf-8
from .forms import LoginForm, RegistrationForm

def reg_forms(request):
	return {
		'login_form': LoginForm(),
		'reg_form': RegistrationForm()
	}

