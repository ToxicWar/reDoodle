# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Room'
        db.create_table('base_room', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
        ))
        db.send_create_signal('base', ['Room'])

        # Adding model 'Chain'
        db.create_table('base_chain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('likes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('isBlocked', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['base.Room'])),
        ))
        db.send_create_signal('base', ['Chain'])


    def backwards(self, orm):
        # Deleting model 'Room'
        db.delete_table('base_room')

        # Deleting model 'Chain'
        db.delete_table('base_chain')


    models = {
        'base.chain': {
            'Meta': {'object_name': 'Chain'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isBlocked': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'likes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['base.Room']"})
        },
        'base.room': {
            'Meta': {'object_name': 'Room'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'})
        }
    }

    complete_apps = ['base']