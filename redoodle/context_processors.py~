# coding: utf-8

t = ""


def test(request):
	global t
	t += "1"
	return {'some_var': "some_text" + t + "-"}


def user(request):
	s = request.session
	#print s['user'] if 'user' in s else 'Anonymous'
	return {'user_name': s['user'] if 'user' in s else 'Anonymous'}
