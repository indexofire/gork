# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing M2M table for field locus on 'MLSTDataSet'
        db.delete_table('mlst_mlstdataset_locus')

        # Adding field 'MLSTLocus.dataset'
        db.add_column(u'mlst_mlstlocus', 'dataset',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', to=orm['mlst.MLSTDataSet']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding M2M table for field locus on 'MLSTDataSet'
        db.create_table(u'mlst_mlstdataset_locus', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mlstdataset', models.ForeignKey(orm[u'mlst.mlstdataset'], null=False)),
            ('mlstlocus', models.ForeignKey(orm[u'mlst.mlstlocus'], null=False))
        ))
        db.create_unique(u'mlst_mlstdataset_locus', ['mlstdataset_id', 'mlstlocus_id'])

        # Deleting field 'MLSTLocus.dataset'
        db.delete_column(u'mlst_mlstlocus', 'dataset_id')


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
        u'mlst.mlstdataset': {
            'Meta': {'ordering': "['name']", 'object_name': 'MLSTDataSet'},
            'creat_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator'", 'to': "orm['gauth.GUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'lastedit_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'moderator': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'moderator'", 'symmetrical': 'False', 'to': "orm['gauth.GUser']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'mlst.mlstlocus': {
            'Meta': {'ordering': "['name']", 'object_name': 'MLSTLocus'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mlst.MLSTDataSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'lastedit_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'mlst.mlstlocusnumber': {
            'Meta': {'ordering': "['creat_time']", 'object_name': 'MLSTLocusNumber'},
            'creat_time': ('django.db.models.fields.DateTimeField', [], {}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'seq_dataset'", 'to': u"orm['mlst.MLSTDataSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['mlst.MLSTLocus']", 'unique': 'True'}),
            'raw': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'seq': ('django.db.models.fields.TextField', [], {}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'mlst.mlststrain': {
            'Meta': {'ordering': "['sttype']", 'unique_together': "(('dataset', 'sttype'),)", 'object_name': 'MLSTStrain'},
            'cc': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'data_source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'strain_dataset'", 'to': u"orm['mlst.MLSTDataSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isolate_country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'isolate_from': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '3'}),
            'isolate_year': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'serotype': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'strain_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'strain_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sttype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'strain_type'", 'to': u"orm['mlst.MLSTType']"}),
            'submit_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submittor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submittor'", 'to': "orm['gauth.GUser']"})
        },
        u'mlst.mlsttype': {
            'Meta': {'ordering': "['value']", 'unique_together': "(('dataset', 'value'),)", 'object_name': 'MLSTType'},
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'type_dataset'", 'to': u"orm['mlst.MLSTDataSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'unique': 'True'})
        }
    }

    complete_apps = ['mlst']