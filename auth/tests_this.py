#coding: utf-8
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail
from auth.forms import RegistrationForm
from django.contrib.auth import SESSION_KEY


class SimpleTest(TestCase):
	
	def test_2x2(self):
		self.assertEqual(2*2, 4, "2x2=4")
	
	def test_registration_get(self):
		resp = self.client.get(reverse('register'))
		self.assertEqual(resp.status_code, 200, "response should be OK")
		self.assertTemplateUsed(resp, 'register.html')
		self.failUnless(isinstance(resp.context['reg_form'], RegistrationForm))
	
	def test_registr_and_login(self):
		#просто регистрируемся
		resp = self.client.post(reverse('register'), data={
			'username': "somename",
			'email': "some@mail.com",
			'password': "somepass"})
		self.assertRedirects(resp, reverse('index'))
		
		#имя занято
		resp = self.client.post(reverse('register'), data={
			'username': "somename",
			'email': "other@mail.com",
			'password': "somepass"})
		self.assertTrue(resp.context['form']['username'].errors)
		self.assertFalse(resp.context['form']['email'].errors)
		
		#почта занята
		resp = self.client.post(reverse('register'), data={
			'username': "othername",
			'email': "some@mail.com",
			'password': "somepass"})
		self.assertFalse(resp.context['form']['username'].errors)
		self.assertTrue(resp.context['form']['email'].errors)
		
		#почта юзера не пруфнута
		user = User.objects.get(email="some@mail.com")
		self.failIf(user.is_active)
		
		
		#ещё не залогинены
		self.assertTrue(SESSION_KEY not in self.client.session)
		
		#неправильное имя
		resp = self.client.post(reverse('login'), data={
			'username': "othername",
			'password': "somepass"})
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(SESSION_KEY not in self.client.session)
		
		#неправильная почта
		resp = self.client.post(reverse('login'), data={
			'username': "somename",
			'password': "otherpass"})
		self.assertEqual(resp.status_code, 200)
		self.assertTrue(SESSION_KEY not in self.client.session)
		
		#всё ок
		resp = self.client.post(reverse('login'), data={
			'username': "somename",
			'password': "somepass"})
		self.assertRedirects(resp, reverse('index'))
		self.assertTrue(SESSION_KEY in self.client.session)
		
		
		#автоматически вписывается почта юзера
		resp = self.client.get(reverse('mail_confirm'))
		self.assertEqual(resp.context['form']['email'].value(), user.email)
		
		#на почте пока пусто
		self.assertEqual(len(mail.outbox), 0)
		
		#подтверждаем
		resp = self.client.post(reverse('mail_confirm'), data={
			'email': "other@mail.com"}, HTTP_HOST='example.com')
		
		#а вот и письмо
		self.assertEqual(len(mail.outbox), 1)
		message = str(mail.outbox[0].message())
		saved_code = user.first_name
		self.assertNotEqual(message.find(saved_code), -1)
		
		
		#разлогинка
		resp = self.client.get(reverse('logout'))
		self.assertTrue(SESSION_KEY not in self.client.session)



