# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Order.web_notified'
        db.add_column(u'spawnsong_order', 'web_notified',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Order.email_notified'
        db.add_column(u'spawnsong_order', 'email_notified',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Order.web_notified'
        db.delete_column(u'spawnsong_order', 'web_notified')

        # Deleting field 'Order.email_notified'
        db.delete_column(u'spawnsong_order', 'email_notified')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'media.audio': {
            'Meta': {'object_name': 'Audio'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'original': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "'NO TITLE'", 'max_length': '255', 'blank': 'True'})
        },
        u'spawnsong.artist': {
            'Meta': {'object_name': 'Artist'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'spawnsong.artistpayment': {
            'Meta': {'object_name': 'ArtistPayment'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spawnsong.Artist']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'paid_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'spawnsong.comment': {
            'Meta': {'ordering': "('created_at',)", 'object_name': 'Comment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'null': 'True', 'blank': 'True'}),
            'is_displayed': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'snippet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spawnsong.Snippet']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'spawnsong.order': {
            'Meta': {'object_name': 'Order'},
            'artist_payment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spawnsong.ArtistPayment']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'email_notified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'purchaser': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'purchaser_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'refunded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'security_token': ('django.db.models.fields.CharField', [], {'default': "'11cd7f8648154c65'", 'max_length': '16'}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spawnsong.Song']"}),
            'stripe_transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'web_notified': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'spawnsong.snippet': {
            'Meta': {'ordering': "('ordering_score', '-created_at')", 'object_name': 'Snippet'},
            'audio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['media.Audio']", 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'echonest_track_analysis': ('jsonfield.fields.JSONField', [], {'default': 'None', 'blank': 'True'}),
            'echonest_track_profile': ('jsonfield.fields.JSONField', [], {'default': 'None', 'blank': 'True'}),
            'genres': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'ordering_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'processing_error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spawnsong.Song']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'initial'", 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'visualisation_effect': ('django.db.models.fields.CharField', [], {'default': "'pulsate'", 'max_length': '20'})
        },
        u'spawnsong.song': {
            'Meta': {'object_name': 'Song'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spawnsong.Artist']"}),
            'complete_audio': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['media.Audio']", 'null': 'True', 'blank': 'True'}),
            'completed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['spawnsong']