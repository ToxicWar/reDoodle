# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'User.salt'
        db.add_column('reg_user', 'salt',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'User.salt'
        db.delete_column('reg_user', 'salt')


    models = {
        'reg.user': {
            'Meta': {'object_name': 'User'},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'})
        }
    }

    complete_apps = ['reg']