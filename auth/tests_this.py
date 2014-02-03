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
	
	def logout(self):
		return self.client.get(reverse('logout'))
	
	def check_mail_and_prove_url_and_check_if_active(self, user, password):
		#письмо на почте
		self.assertEqual(len(mail.outbox), 1)
		message = str(mail.outbox[0].message())
		saved_code = user.first_name
		code_start_pos = message.find(saved_code)
		self.assertNotEqual(code_start_pos, -1, "code should have been sended")
		url_start_pos = message[:code_start_pos].rfind("http://")
		url = message[url_start_pos : code_start_pos+len(saved_code)]
		
		#подтверждаем, не залогинившись
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 302)
		self.assertFalse(User.objects.get(username=user.username).is_active)
		#залогинившись
		self.login(user.username, password)
		resp = self.client.get(url)
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(User.objects.get(username=user.username).is_active)
	
	
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
		self.assertEqual(resp.status_code, 200)
		User.objects.get(username="somename")
		
		#имя занято
		resp = self.register("somename", "other@mail.com", "somepass")
		self.assertEqual(resp.status_code, 400)
		err = json.loads(resp.content)['errors']
		self.assertTrue('username' in err)
		self.assertFalse('password' in err)
		
		#почта занята
		resp = self.register("othername", "some@mail.com", "somepass")
		self.assertEqual(resp.status_code, 400)
		err = json.loads(resp.content)['errors']
		self.assertFalse('username' in err)
		self.assertTrue('email' in err)
		self.assertFalse('password' in err)
		
		#почта юзера не пруфнута
		user = User.objects.get(email="some@mail.com")
		self.failIf(user.is_active)
	
	def test_registration_without_mail(self):
		resp = self.register("somename", None, "somepass")
		self.assertEqual(resp.status_code, 200)
		#мыло-не мыло, а пользователь должен создаться
		User.objects.get(username="somename")
		
		#была бага: второй юзер с пустой почтой не мог создаться,
		#потому что эта (пустая) почта уже занята
		resp = self.register("othername", None, "somepass")
		self.assertEqual(resp.status_code, 200)
		User.objects.get(username="othername")
	
	def test_login(self):
		self.register("somename", "some@mail.com", "somepass")
		
		#ещё не залогинены
		self.assertTrue(SESSION_KEY not in self.client.session)
		
		#неправильное имя
		resp = self.login("othername", "somepass")
		self.assertEqual(resp.status_code, 400)
		err = json.loads(resp.content)['errors']
		self.assertTrue('username' in err)
		self.assertTrue(SESSION_KEY not in self.client.session)
		
		#неправильнный пароль
		resp = self.login("somename", "otherpass")
		self.assertEqual(resp.status_code, 400)
		err = json.loads(resp.content)['errors']
		self.assertTrue('password' in err)
		self.assertTrue(SESSION_KEY not in self.client.session)
		
		#всё ок
		resp = self.login("somename", "somepass")
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(SESSION_KEY in self.client.session)
	
	def test_mail_confirm_when_register_with_mail(self):
		self.register("somename", "some@mail.com", "somepass")
		user = User.objects.get(username="somename")
		self.assertFalse(user.is_active)
		
		self.check_mail_and_prove_url_and_check_if_active(user, "somepass")
	
	def test_mail_confirm_when_register_without_mail(self):
		self.register("somename", None, "somepass")
		
		#на почте пока пусто
		self.assertEqual(len(mail.outbox), 0)
		
		#отправляем
		def send_mail():
			return self.client.post(reverse('mail_confirm'), data={
				'email': "zblzlo4ui@yandex.ru"}, HTTP_HOST='testserver')
		#не залогинившись
		resp = send_mail()
		self.assertEqual(resp.status_code, 302)
		#залогинившись
		self.login("somename", "somepass")
		resp = send_mail()
		self.assertEqual(resp.status_code, 200)
		
		user = User.objects.get(username="somename")
		self.assertFalse(user.is_active)
		self.logout()
		
		self.check_mail_and_prove_url_and_check_if_active(user, "somepass")
	
	def test_logout(self):
		self.register("somename", "some@mail.com", "somepass")
		self.login("somename", "somepass")
		
		#разлогинка
		resp = self.logout()
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(SESSION_KEY not in self.client.session)
