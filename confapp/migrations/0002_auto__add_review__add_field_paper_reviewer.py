# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Review'
        db.create_table('confapp_review', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paper', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['confapp.Paper'], unique=True)),
            ('original', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('significant', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('clear', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('correct', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('citing', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('figures', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('adequacy', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('novelty', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('summary', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('remarks', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('confapp', ['Review'])

        # Adding field 'Paper.reviewer'
        db.add_column('confapp_paper', 'reviewer',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='review_papers', null=True, to=orm['confapp.Account']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Review'
        db.delete_table('confapp_review')

        # Deleting field 'Paper.reviewer'
        db.delete_column('confapp_paper', 'reviewer_id')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'confapp.account': {
            'Meta': {'object_name': 'Account'},
            'accounttype': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['confapp.AccountType']"}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address2': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'nip': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'confapp.accounttype': {
            'Meta': {'object_name': 'AccountType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'payment': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        },
        'confapp.attachment': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Attachment'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paper': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['confapp.Paper']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'confapp.conference': {
            'Meta': {'object_name': 'Conference'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'confapp.paper': {
            'Meta': {'object_name': 'Paper'},
            'abstract': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['confapp.Account']"}),
            'authors': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reviewer': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'review_papers'", 'null': 'True', 'to': "orm['confapp.Account']"}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['confapp.SessionType']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'confapp.review': {
            'Meta': {'object_name': 'Review'},
            'adequacy': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'citing': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'clear': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'correct': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'figures': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'novelty': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'original': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'paper': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['confapp.Paper']", 'unique': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'remarks': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'significant': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'summary': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'confapp.sessiontype': {
            'Meta': {'object_name': 'SessionType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['confapp']