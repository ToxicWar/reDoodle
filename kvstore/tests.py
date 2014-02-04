# coding: utf-8
from django.test import TestCase
from .models import KV


class SimpleTest(TestCase):
	
	def test_basic_addition(self):
		"""
		Tests that 1 + 1 always equals 2.
		"""
		self.assertEqual(1 + 1, 2)
	
	def test_basic(self):
		"""
		Tests that some basic values vill be processed properly.
		"""
		values = {
			'int': 42,
			'string': 'Hello World!',
			'строка': 'Привет Мир!',
			'array': [1, '2'],
			'hashmap': {1:2, '3': '4'}
		}
		for key, val in values.items():
			self.assertIsNone(KV.get(key), 'should return None as default')
			self.assertEqual(KV.get(key, 'def val'), 'def val', 'should return default value')
			KV.put(key, val)
			self.assertEqual(KV.get(key), val, 'should return saved value')
			KV.rm(key)
			self.assertIsNone(KV.get(key), 'record should have been removed')
	
	def test_exists(self):
		"""
		Tests that value will be replaced for similar key.
		"""
		KV.put('key', 'val')
		KV.put('key', 'another val')
		self.assertEqual(KV.get('key'), 'another val')

