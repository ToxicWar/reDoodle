# coding: utf-8
# http://imbolc.name/2009/12/key-value-django-orm.html
from django.db import models
from picklefield.fields import PickledObjectField

class KV(models.Model):
	key = models.CharField(u'Key', max_length=50, unique=True)
	val = PickledObjectField(u'Value')

	@classmethod
	def get(self, key, default=None):
		try:
			return self.objects.get(key=key).val
		except self.DoesNotExist:
			return default

	@classmethod
	def put(self, key, val):
		obj, new = self.objects.get_or_create(key=key)
		obj.val = val
		obj.save()

	@classmethod
	def rm(self, key):
		try:
			self.objects.get(key=key).delete()
		except self.DoesNotExist:
			pass
