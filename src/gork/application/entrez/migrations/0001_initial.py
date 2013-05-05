# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EntrezTerm'
        db.create_table(u'entrez_entrezterm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='term_owner', to=orm['auth.User'])),
            ('period', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=7)),
            ('db', self.gf('django.db.models.fields.CharField')(default='pubmed', max_length=30)),
            ('creation_date', self.gf('django.db.models.fields.DateField')(blank=True)),
            ('lastedit_date', self.gf('django.db.models.fields.DateField')(blank=True)),
        ))
        db.send_create_signal(u'entrez', ['EntrezTerm'])

        # Adding model 'EntrezEntry'
        db.create_table(u'entrez_entrezentry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eid', self.gf('django.db.models.fields.CharField')(default='', max_length=20)),
            ('raw', self.gf('django.db.models.fields.TextField')(default='')),
            ('term', self.gf('django.db.models.fields.related.ForeignKey')(related_name='entry_term', to=orm['entrez.EntrezTerm'])),
            ('content', self.gf('django.db.models.fields.TextField')(default='')),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('magzine', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('authors', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('abstract', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('read', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('creation_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastedit_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'entrez', ['EntrezEntry'])


    def backwards(self, orm):
        # Deleting model 'EntrezTerm'
        db.delete_table(u'entrez_entrezterm')

        # Deleting model 'EntrezEntry'
        db.delete_table(u'entrez_entrezentry')


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
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'entrez.entrezentry': {
            'Meta': {'ordering': "['-creation_time']", 'object_name': 'EntrezEntry'},
            'abstract': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'authors': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'eid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastedit_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'magzine': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'raw': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'read': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'term': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entry_term'", 'to': u"orm['entrez.EntrezTerm']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        },
        u'entrez.entrezterm': {
            'Meta': {'ordering': "['-creation_date']", 'object_name': 'EntrezTerm'},
            'creation_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'db': ('django.db.models.fields.CharField', [], {'default': "'pubmed'", 'max_length': '30'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastedit_date': ('django.db.models.fields.DateField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'term_owner'", 'to': u"orm['auth.User']"}),
            'period': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '7'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '512'})
        }
    }

    complete_apps = ['entrez']