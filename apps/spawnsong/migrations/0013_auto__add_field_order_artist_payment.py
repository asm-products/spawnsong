# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Order.artist_payment'
        db.add_column(u'spawnsong_order', 'artist_payment',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['spawnsong.ArtistPayment']),
                      keep_default=False)

        # Removing M2M table for field orders on 'ArtistPayment'
        db.delete_table('spawnsong_artistpayment_orders')


    def backwards(self, orm):
        # Deleting field 'Order.artist_payment'
        db.delete_column(u'spawnsong_order', 'artist_payment_id')

        # Adding M2M table for field orders on 'ArtistPayment'
        db.create_table(u'spawnsong_artistpayment_orders', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artistpayment', models.ForeignKey(orm[u'spawnsong.artistpayment'], null=False)),
            ('order', models.ForeignKey(orm[u'spawnsong.order'], null=False))
        ))
        db.create_unique(u'spawnsong_artistpayment_orders', ['artistpayment_id', 'order_id'])


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'purchaser': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'purchaser_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'refunded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'security_token': ('django.db.models.fields.CharField', [], {'default': "'ab951f1411da4aff'", 'max_length': '16'}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spawnsong.Song']"}),
            'stripe_transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'spawnsong.snippet': {
            'Meta': {'ordering': "('ordering_score', '-created_at')", 'object_name': 'Snippet'},
            'audio_mp3': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'echonest_track_analysis': ('jsonfield.fields.JSONField', [], {'default': 'None', 'blank': 'True'}),
            'echonest_track_profile': ('jsonfield.fields.JSONField', [], {'default': 'None', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '100'}),
            'ordering_score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'processing_error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spawnsong.Song']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'processing'", 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploaded_audio': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'visualisation_effect': ('django.db.models.fields.CharField', [], {'default': "'pulsate'", 'max_length': '20'})
        },
        u'spawnsong.song': {
            'Meta': {'object_name': 'Song'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spawnsong.Artist']"}),
            'complete_audio': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'completed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['spawnsong']