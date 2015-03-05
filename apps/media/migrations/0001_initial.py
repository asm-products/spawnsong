# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Audio'
        db.create_table(u'media_audio', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('original', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
        ))
        db.send_create_signal(u'media', ['Audio'])

        # Adding model 'AudioFormat'
        db.create_table(u'media_audioformat', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('audio', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['media.Audio'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('state', self.gf('django.db.models.fields.CharField')(default='initial', max_length=20)),
            ('last_error', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('profile', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('audio_data', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'media', ['AudioFormat'])


    def backwards(self, orm):
        # Deleting model 'Audio'
        db.delete_table(u'media_audio')

        # Deleting model 'AudioFormat'
        db.delete_table(u'media_audioformat')


    models = {
        u'media.audio': {
            'Meta': {'object_name': 'Audio'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'media.audioformat': {
            'Meta': {'object_name': 'AudioFormat'},
            'audio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['media.Audio']"}),
            'audio_data': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'profile': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'initial'", 'max_length': '20'})
        }
    }

    complete_apps = ['media']