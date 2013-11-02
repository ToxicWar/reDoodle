#coding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail
from auth.forms import RegistrationForm
from django.contrib.auth import SESSION_KEY
import json


class SimpleTest(TestCase):
	
	def register(self, name, mail, passwd):
		data = {'username': name, 'password': passwd}
		if (mail):
			data['email'] = mail
		return self.client.post(reverse('register'),
			data=data, HTTP_HOST='testserver')
	
	def login(self, name, passwd):
		return self.client.post(reverse('login'), data={
			'username': name,
			'password': passwd}, HTTP_HOST='testserver')
	
	def test_2x2(self):
		self.assertEqual(2*2, 4, "2x2=4")
	
	def test_login_get(self):
		resp = self.client.get(reverse('login'))
		self.assertEqual(resp.status_code, 404, "only POSTs are allowed")
	
	def test_registration_get(self):
		resp = self.client.get(reverse('register'))
		self.assertEqual(resp.status_code, 404, "only POSTs are allowed")
	
	def test_registration(self):
		#просто регистрируемся
		resp = self.register("somename", "some@mail.com", "somepass")
		self.assertJSONEqual(resp.content, '{"result": "ok"}')
		User.objects.get(username="somename")
		
		#имя занято
		resp = self.register("somename", "other@mail.com", "somepass")
		err = json.loads(resp.content)['errors']
		self.assertTrue('username' in err)
		self.assertFalse('password' in err)
		
		#почта занята
		resp = self.register("othername", "some@mail.com", "somepass")
		err = json.loads(resp.content)['errors']
		self.assertFalse('username' in err)
		self.assertTrue('email' in err)
		self.assertFalse('password' in err)
		
		#почта юзера не пруфнута
		user = User.objects.get(email="some@mail.com")
		self.failIf(user.is_active)
	
	def test_registration_without_mail(self):
		resp = self.register("somename", None, "somepass")
		#мыло-не мыло, а пользователь должен создаться
		User.objects.get(username="somename")
		
		#была бага: второй юзер с пустой почтой не мог создаться,
		#потому что эта (пустая) почта уже занята
		resp = self.register("othername", None, "somepass")
		User.objects.get(username="othername")
	
	def test_login(self):
		self.register("somename", "some@mail.com", "somepass")
		
		#ещё не залогинены
		self.assertTrue(SESSION_KEY not in self.client.session)
		
		#неправильное имя
		resp = self.login("othername", "somepass")
		err = json.loads(resp.content)['errors']
		self.assertTrue('username' in err)
		self.assertTrue(SESSION_KEY not in self.client.session)
		
		#неправильнный пароль
		resp = self.login("somename", "otherpass")
		err = json.loads(resp.content)['errors']
		self.assertTrue('password' in err)
		self.assertTrue(SESSION_KEY not in self.client.session)
		
		#всё ок
		resp = self.login("somename", "somepass")
		self.assertJSONEqual(resp.content, '{"result": "ok"}')
		self.assertTrue(SESSION_KEY in self.client.session)
	
	"""def test_mail_confirm_when_register_with_mail(self):
		self.register("somename", "some@mail.com", "somepass")
		user = User.objects.get(username="somename")
		self.client.get(reverse('login')) # тут установится тестовая кука
		self.login("somename", "somepass")
		
		#в подтверждалку автоматически вписывается почта юзера
		resp = self.client.get(reverse('mail_confirm'))
		print resp
		self.assertEqual(resp.context['form']['email'].value(), user.email)
		
		#письмо на почту уже отправлено
		self.assertEqual(len(mail.outbox), 1)
		message = str(mail.outbox[0].message())
		saved_code = user.first_name
		self.assertNotEqual(message.find(saved_code), -1)
	
	def test_mail_confirm_when_register_without_mail(self):
		self.register("somename", None, "somepass")
		user = User.objects.get(username="somename")
		self.client.get(reverse('login')) # тут установится тестовая кука
		self.login("somename", "somepass")
		
		#на почте пока пусто
		self.assertEqual(len(mail.outbox), 0)
		
		#подтверждаем
		resp = self.client.post(reverse('mail_confirm'), data={
			'email': "zblzlo4ui@yandex.ru"}, HTTP_HOST='testserver')
		
		#а вот и письмо
		self.assertEqual(len(mail.outbox), 1)
		message = str(mail.outbox[0].message())
		saved_code = user.first_name
		self.assertNotEqual(message.find(saved_code), -1)
	
	def test_logout(self):
		self.register("somename", "some@mail.com", "somepass")
		self.login("somename", "somepass")
		
		#разлогинка
		resp = self.client.get(reverse('logout'))
		self.assertTrue(SESSION_KEY not in self.client.session)"""



