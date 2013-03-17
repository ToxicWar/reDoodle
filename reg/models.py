from django.db import models
from django.utils.translation import ugettext_lazy as _
import string
import random
from hashlib import sha1


class User(models.Model):
	name = models.CharField(_(u'Name'), max_length=255, null=False)
	mail = models.EmailField(_(u'Mail'))
	hash = models.CharField('Hash', max_length=255, null=False)
	salt = models.CharField('Salt', max_length=32, null=True)

	class Meta:
		verbose_name = 'User'
		verbose_name_plural = 'Users'

	def __unicode__(self):
		return self.name

	def new_pass2hash(self, password):
		symbols = string.ascii_letters + string.digits
		self.salt = ''.join(random.choice(symbols) for i in range(15))
		self.hash = sha1(self.salt + password).hexdigest()

	def check_pass(self, password):
		return self.hash == sha1(self.salt + password).hexdigest()
