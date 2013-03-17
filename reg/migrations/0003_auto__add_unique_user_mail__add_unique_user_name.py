# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'User', fields ['mail']
        db.create_unique('reg_user', ['mail'])

        # Adding unique constraint on 'User', fields ['name']
        db.create_unique('reg_user', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'User', fields ['name']
        db.delete_unique('reg_user', ['name'])

        # Removing unique constraint on 'User', fields ['mail']
        db.delete_unique('reg_user', ['mail'])


    models = {
        'reg.user': {
            'Meta': {'object_name': 'User'},
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'})
        }
    }

    complete_apps = ['reg']
