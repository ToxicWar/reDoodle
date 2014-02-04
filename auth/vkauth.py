#coding: utf-8
import httplib


APP_ID = "3751612";
APP_SECRET = "HqYk9YvHvcreFR8OAlXs";

c = httplib.HTTPSConnection("oauth.vk.com")
c.request(
	"GET",
	"/access_token"+
		"?client_id="+APP_ID+
		"&client_secret="+APP_SECRET+
		"&grant_type=client_credentials")
response = c.getresponse()
print response.status, response.reason
data = response.read()
print data


# http://vk.com/dev/secure_how_to
# Серверное API, бла-бла-бла access_token.
# Для получения оного необходимо выполнить запрос к:
# https://oauth.vk.com/access_token
#  * client_id = APP_ID
#  * client_secret = APP_SECRET
#  * grant_type = "client_credentials" *прям вот эту строчку*
# Результат типа:
# {"access_token":"533bacf01e11f55b536a565b57531ac114461ae8736d6506a3"}
# НО НА САМОМ ДЕЛЕ в ответ приходит client_secret, а НЕ access_token,
# но в запросх его надо ВСЁ РАВНО писать в параметр access_token

# http://vk.com/dev/secure.checkToken
# Валидность пользователя по IP
# https://api.vk.com/method/secure.checkToken
#  * client_secret = APP_SECRET *именно АПП клиент aka юзер тут ни при чём*
#  * token = token *ВНИМАНИЕ!!! приходит в параметре с именем access_token! не путать со следующим!*
#  * access_token = access_token *с первого этапа, не путать с токеном*
#  * ip = вычисляемый ip *ну хоть тут всё очевидно*

