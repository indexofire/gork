# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'EntrezEntry.owner'
        db.alter_column(u'entrez_entrezentry', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gauth.GUser']))
        # Adding field 'EntrezTerm.unreads'
        db.add_column(u'entrez_entrezterm', 'unreads',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


        # Changing field 'EntrezTerm.owner'
        db.alter_column(u'entrez_entrezterm', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gauth.GUser']))

    def backwards(self, orm):

        # Changing field 'EntrezEntry.owner'
        db.alter_column(u'entrez_entrezentry', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))
        # Deleting field 'EntrezTerm.unreads'
        db.delete_column(u'entrez_entrezterm', 'unreads')


        # Changing field 'EntrezTerm.owner'
        db.alter_column(u'entrez_entrezterm', 'owner_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User']))

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
            'authors': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'creation_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'db': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'eid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastedit_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'magzine': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'entry_owner'", 'to': "orm['gauth.GUser']"}),
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
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'term_owner'", 'to': "orm['gauth.GUser']"}),
            'period': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '7'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'unreads': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'gauth.guser': {
            'Meta': {'ordering': "['-date_joined']", 'object_name': 'GUser'},
            'about_me': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'about_me_html': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'avatar': ('imagekit.models.fields.ProcessedImageField', [], {'default': "'/media/avatars/default.png'", 'max_length': '100'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'bronze_badges': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_visited': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '75', 'blank': 'True'}),
            'gender': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '3', 'blank': 'True'}),
            'gold_badges': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '15', 'blank': 'True'}),
            'new_messages': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'qa_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'scholar': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'silver_badges': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'user_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30', 'db_index': 'True'})
        }
    }

    complete_apps = ['entrez']