# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Conference'
        db.create_table('confapp_conference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('confapp', ['Conference'])

        # Adding model 'Account'
        db.create_table('confapp_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('institute', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('nip', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('accounttype', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['confapp.AccountType'])),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address2', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('confapp', ['Account'])

        # Adding model 'AccountType'
        db.create_table('confapp_accounttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('payment', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
        ))
        db.send_create_signal('confapp', ['AccountType'])

        # Adding model 'Paper'
        db.create_table('confapp_paper', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['confapp.Account'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('authors', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('abstract', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('session', self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['confapp.SessionType'])),
        ))
        db.send_create_signal('confapp', ['Paper'])

        # Adding model 'SessionType'
        db.create_table('confapp_sessiontype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('confapp', ['SessionType'])

        # Adding model 'Attachment'
        db.create_table('confapp_attachment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('paper', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['confapp.Paper'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('confapp', ['Attachment'])


    def backwards(self, orm):
        # Deleting model 'Conference'
        db.delete_table('confapp_conference')

        # Deleting model 'Account'
        db.delete_table('confapp_account')

        # Deleting model 'AccountType'
        db.delete_table('confapp_accounttype')

        # Deleting model 'Paper'
        db.delete_table('confapp_paper')

        # Deleting model 'SessionType'
        db.delete_table('confapp_sessiontype')

        # Deleting model 'Attachment'
        db.delete_table('confapp_attachment')


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
            'session': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': "orm['confapp.SessionType']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
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