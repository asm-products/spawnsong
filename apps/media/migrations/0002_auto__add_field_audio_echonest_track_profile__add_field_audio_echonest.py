# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Audio.echonest_track_profile'
        db.add_column(u'media_audio', 'echonest_track_profile',
                      self.gf('jsonfield.fields.JSONField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Audio.echonest_track_analysis'
        db.add_column(u'media_audio', 'echonest_track_analysis',
                      self.gf('jsonfield.fields.JSONField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Audio.echonest_track_profile'
        db.delete_column(u'media_audio', 'echonest_track_profile')

        # Deleting field 'Audio.echonest_track_analysis'
        db.delete_column(u'media_audio', 'echonest_track_analysis')


    models = {
        u'media.audio': {
            'Meta': {'object_name': 'Audio'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'echonest_track_analysis': ('jsonfield.fields.JSONField', [], {'default': 'None', 'blank': 'True'}),
            'echonest_track_profile': ('jsonfield.fields.JSONField', [], {'default': 'None', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'NO TITLE'", 'max_length': '255', 'blank': 'True'})
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