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
