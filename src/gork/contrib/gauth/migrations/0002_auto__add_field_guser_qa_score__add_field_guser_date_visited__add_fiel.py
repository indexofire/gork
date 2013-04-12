# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GUser.qa_score'
        db.add_column(u'gauth_guser', 'qa_score',
                      self.gf('django.db.models.fields.IntegerField')(default=0, blank=True),
                      keep_default=False)

        # Adding field 'GUser.date_visited'
        db.add_column(u'gauth_guser', 'date_visited',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'GUser.scholar'
        db.add_column(u'gauth_guser', 'scholar',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'GUser.user_type'
        db.add_column(u'gauth_guser', 'user_type',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'GUser.about_me'
        db.add_column(u'gauth_guser', 'about_me',
                      self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True),
                      keep_default=False)

        # Adding field 'GUser.about_me_html'
        db.add_column(u'gauth_guser', 'about_me_html',
                      self.gf('django.db.models.fields.TextField')(default='', null=True, blank=True),
                      keep_default=False)

        # Adding field 'GUser.bronze_badges'
        db.add_column(u'gauth_guser', 'bronze_badges',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'GUser.silver_badges'
        db.add_column(u'gauth_guser', 'silver_badges',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'GUser.gold_badges'
        db.add_column(u'gauth_guser', 'gold_badges',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'GUser.new_messages'
        db.add_column(u'gauth_guser', 'new_messages',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GUser.qa_score'
        db.delete_column(u'gauth_guser', 'qa_score')

        # Deleting field 'GUser.date_visited'
        db.delete_column(u'gauth_guser', 'date_visited')

        # Deleting field 'GUser.scholar'
        db.delete_column(u'gauth_guser', 'scholar')

        # Deleting field 'GUser.user_type'
        db.delete_column(u'gauth_guser', 'user_type')

        # Deleting field 'GUser.about_me'
        db.delete_column(u'gauth_guser', 'about_me')

        # Deleting field 'GUser.about_me_html'
        db.delete_column(u'gauth_guser', 'about_me_html')

        # Deleting field 'GUser.bronze_badges'
        db.delete_column(u'gauth_guser', 'bronze_badges')

        # Deleting field 'GUser.silver_badges'
        db.delete_column(u'gauth_guser', 'silver_badges')

        # Deleting field 'GUser.gold_badges'
        db.delete_column(u'gauth_guser', 'gold_badges')

        # Deleting field 'GUser.new_messages'
        db.delete_column(u'gauth_guser', 'new_messages')


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
        },
        'gauth.role': {
            'Meta': {'object_name': 'Role'},
            '_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'roles'", 'blank': 'True', 'db_column': "'permissions'", 'to': u"orm['auth.Permission']"}),
            '_users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'_roles'", 'blank': 'True', 'db_column': "'users'", 'to': "orm['gauth.GUser']"}),
            'codename': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['gauth.Role']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['gauth']