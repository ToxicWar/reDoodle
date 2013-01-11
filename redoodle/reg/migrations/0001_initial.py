# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table('reg_user', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('reg', ['User'])


    def backwards(self, orm):
        # Deleting model 'User'
        db.delete_table('reg_user')


    models = {
        'reg.user': {
            'Meta': {'object_name': 'User'},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['reg']