#coding: utf-8
import httplib
import json
from kvstore.models import KV
from datetime import timedelta, datetime


APP_ID = "3751612"
APP_SECRET = "HqYk9YvHvcreFR8OAlXs"
# теоретически токен экспайриться не должен
# практически - ... кто его знает
ACCESS_TOKEN_TIMEOUT = timedelta(hours=1) # мб где-нибудь день. мб неделю


def simpleGET(host, params):
	#TODO: мб лучше будет держать одно соединение, переоткрывать при надобности
	conn = httplib.HTTPSConnection(host)
	conn.request("GET", params)
	#print res.status, res.reason
	data = conn.getresponse().read()
	conn.close()
	return data


print "Initialising VK module..."

access_token = KV.get('vk_access_token')
if access_token:
	print '  ...found saved access_token'
	if datetime.now() > KV.get('vk_access_token_expire'):
		print '  ...which has expired'
		access_token = None

if not access_token:
	print '  ...trying to register APP on VK'
	
	data = simpleGET(
		"oauth.vk.com",
		"/access_token"+
			"?client_id="+APP_ID+
			"&client_secret="+APP_SECRET+
			"&grant_type=client_credentials")
	#думаю, невалидный ЖСОН от вконтача не пойдёт, можно не try-except'ить
	data = json.loads(data)
	
	if "error" in data:
		raise ImproperlyConfigured(
			'Failed to get access_token:\n' + data['error'] + '\n' +
			'Full response:\n' + data)
	
	access_token = data['access_token']
	KV.put('vk_access_token', access_token)
	KV.put('vk_access_token_expire', datetime.now() + ACCESS_TOKEN_TIMEOUT)
	print '  ...data: ', data  # 'expires_in'

print "  ...success!"


def proof_ip(request):
	token = request.GET['access_token']#check
	pi = request.META.REMOTE_ADDR
	print token, pi
	data = simpleGET(
		'api.vk.com',
		'/method/secure.checkToken'+
			'?client_secret='+APP_SECRET+
			'&token='+token+
			'&access_token='+KV.get('vk_access_token')+
			'&ip='+ip)
	print data



#{"error":{"error_code":5,"error_msg":"User authorization failed: no access_token passed.","request_params":[{"key":"oauth","value":"1"},{"key":"method","value":"secure.checkToken"}]}}

# http://vk.com/dev/secure_how_to
# Серверное API, бла-бла-бла access_token.
# Для получения оного необходимо выполнить запрос к:
# https://oauth.vk.com/access_token
#  * client_id = APP_ID
#  * client_secret = APP_SECRET
#  * grant_type = "client_credentials" *прям вот эту строчку*
# Результат типа:
# {"access_token":"533bacf01e11f55b536a565b57531ac114461ae8736d6506a3"}

# http://vk.com/dev/secure.checkToken
# Валидность пользователя по IP
# https://api.vk.com/method/secure.checkToken
#  * client_secret = APP_SECRET *именно АПП; клиент aka юзер тут ни при чём*
#  * token = token *ВНИМАНИЕ!!! приходит в параметре с именем access_token! не путать со следующим!*
#  * access_token = access_token *с первого этапа, не путать с токеном*
#  * ip = вычисляемый ip *ну хоть тут всё очевидно*

