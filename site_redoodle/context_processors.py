# coding: utf-8


def user(request):
	s = request.session
	return {'user_name': s['user'] if 'user' in s else 'Anonymous'}
