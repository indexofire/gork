# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'EntrezEntry.db'
        db.add_column(u'entrez_entrezentry', 'db',
                      self.gf('django.db.models.fields.CharField')(default='pubmed', max_length=30),
                      keep_default=False)

        # Adding field 'EntrezEntry.owner'
        db.add_column(u'entrez_entrezentry', 'owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='entry_owner', to=orm['auth.User']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'EntrezEntry.db'
        db.delete_column(u'entrez_entrezentry', 'db')

        # Deleting field 'EntrezEntry.owner'
        db.delete_column(u'entrez_entrezentry', 'owner_id')


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
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'db': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'eid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastedit_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'magzine': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entry_owner'", 'to': u"orm['auth.User']"}),
            'raw': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
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