# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Snippet'
        db.create_table(u'spawnsong_snippet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('song', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spawnsong.Song'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('state', self.gf('django.db.models.fields.CharField')(default='processing', max_length=20)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('audio', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('echonest_data', self.gf('jsonfield.fields.JSONField')(blank=True)),
            ('visualisation_effect', self.gf('django.db.models.fields.CharField')(default='pulsate', max_length=20)),
        ))
        db.send_create_signal(u'spawnsong', ['Snippet'])

        # Adding model 'Song'
        db.create_table(u'spawnsong_song', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('artist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spawnsong.Artist'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('complete_audio', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True)),
            ('completed_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal(u'spawnsong', ['Song'])

        # Adding model 'Artist'
        db.create_table(u'spawnsong_artist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'spawnsong', ['Artist'])

        # Adding model 'Comment'
        db.create_table(u'spawnsong_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('snippet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spawnsong.Snippet'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('ip_address', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, null=True, blank=True)),
            ('is_displayed', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'spawnsong', ['Comment'])

        # Adding model 'Order'
        db.create_table(u'spawnsong_order', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('song', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spawnsong.Song'])),
            ('purchaser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('price', self.gf('django.db.models.fields.IntegerField')()),
            ('refunded', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('delivered', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('stripe_transaction_id', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'spawnsong', ['Order'])

        # Adding model 'ArtistPayment'
        db.create_table(u'spawnsong_artistpayment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('arist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spawnsong.Artist'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'spawnsong', ['ArtistPayment'])

        # Adding M2M table for field orders on 'ArtistPayment'
        db.create_table(u'spawnsong_artistpayment_orders', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('artistpayment', models.ForeignKey(orm[u'spawnsong.artistpayment'], null=False)),
            ('order', models.ForeignKey(orm[u'spawnsong.order'], null=False))
        ))
        db.create_unique(u'spawnsong_artistpayment_orders', ['artistpayment_id', 'order_id'])


    def backwards(self, orm):
        # Deleting model 'Snippet'
        db.delete_table(u'spawnsong_snippet')

        # Deleting model 'Song'
        db.delete_table(u'spawnsong_song')

        # Deleting model 'Artist'
        db.delete_table(u'spawnsong_artist')

        # Deleting model 'Comment'
        db.delete_table(u'spawnsong_comment')

        # Deleting model 'Order'
        db.delete_table(u'spawnsong_order')

        # Deleting model 'ArtistPayment'
        db.delete_table(u'spawnsong_artistpayment')

        # Removing M2M table for field orders on 'ArtistPayment'
        db.delete_table('spawnsong_artistpayment_orders')


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
            'arist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spawnsong.Artist']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'orders': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['spawnsong.Order']", 'symmetrical': 'False'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'spawnsong.comment': {
            'Meta': {'object_name': 'Comment'},
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'delivered': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {}),
            'purchaser': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'refunded': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spawnsong.Song']"}),
            'stripe_transaction_id': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'spawnsong.snippet': {
            'Meta': {'object_name': 'Snippet'},
            'audio': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'echonest_data': ('jsonfield.fields.JSONField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'song': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spawnsong.Song']"}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'processing'", 'max_length': '20'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'visualisation_effect': ('django.db.models.fields.CharField', [], {'default': "'pulsate'", 'max_length': '20'})
        },
        u'spawnsong.song': {
            'Meta': {'object_name': 'Song'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['spawnsong.Artist']"}),
            'complete_audio': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'completed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['spawnsong']