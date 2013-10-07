#coding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail
from auth.forms import RegistrationForm
from django.contrib.auth import SESSION_KEY


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
	
	def test_registration_get(self):
		resp = self.client.get(reverse('register'))
		self.assertEqual(resp.status_code, 200, "response should be OK")
		self.assertTemplateUsed(resp, 'register.html')
		self.failUnless(isinstance(resp.context['reg_form'], RegistrationForm))
	
	def test_registration(self):
		#просто регистрируемся
		resp = self.register("somename", "some@mail.com", "somepass")
		self.assertRedirects(resp, reverse('index'))
		
		#имя занято
		resp = self.register("somename", "other@mail.com", "somepass")
		self.assertTrue(resp.context['form']['username'].errors)
		self.assertFalse(resp.context['form']['email'].errors)
		
		#почта занята
		resp = self.register("othername", "some@mail.com", "somepass")
		self.assertFalse(resp.context['form']['username'].errors)
		self.assertTrue(resp.context['form']['email'].errors)
		
		#почта юзера не пруфнута
		user = User.objects.get(email="some@mail.com")
		self.failIf(user.is_active)
	
	def test_registration_without_mail(self):
		resp = self.register("somename", None, "somepass")
		self.assertRedirects(resp, reverse('index'))
	
	def test_login(self):
		self.register("somename", "some@mail.com", "somepass")
		
		#ещё не залогинены
		self.assertTrue(SESSION_KEY not in self.client.session)
		
		#неправильное имя
		resp = self.login("othername", "somepass")
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(SESSION_KEY not in self.client.session)
		
		#неправильная почта
		resp = self.login("somename", "otherpass")
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(SESSION_KEY not in self.client.session)
		
		#всё ок
		resp = self.login("somename", "somepass")
		self.assertRedirects(resp, reverse('index'))
		self.assertTrue(SESSION_KEY in self.client.session)
	
	def test_mail_confirm_when_register_with_mail(self):
		self.register("somename", "some@mail.com", "somepass")
		user = User.objects.get(username="somename")
		self.login("somename", "somepass")
		
		#в подтверждалку автоматически вписывается почта юзера
		resp = self.client.get(reverse('mail_confirm'))
		self.assertEqual(resp.context['form']['email'].value(), user.email)
		
		#письмо на почту уже отправлено
		self.assertEqual(len(mail.outbox), 1)
		message = str(mail.outbox[0].message())
		saved_code = user.first_name
		self.assertNotEqual(message.find(saved_code), -1)
	
	def test_mail_confirm_when_register_without_mail(self):
		self.register("somename", None, "somepass")
		user = User.objects.get(username="somename")
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
		self.assertTrue(SESSION_KEY not in self.client.session)



