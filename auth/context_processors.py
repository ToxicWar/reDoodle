def reg_forms(request):
	login_form = "login form will be there"
	reg_form = "registration form will be there"
	print "hello from cp!"
	if hasattr(request, 'login_form'):
		print "lf found", request.login_form
	else:
		print "not found"
	request.login_form = "login form from cp"
	return {}

