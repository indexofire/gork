# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'MLSTType', fields ['dataset', 'value']
        db.delete_unique(u'mlst_mlsttype', ['dataset_id', 'value'])

        # Removing unique constraint on 'MLSTStrain', fields ['dataset', 'sttype']
        db.delete_unique(u'mlst_mlststrain', ['dataset_id', 'sttype_id'])

        # Deleting model 'MLSTDataSet'
        db.delete_table(u'mlst_mlstdataset')

        # Removing M2M table for field moderator on 'MLSTDataSet'
        db.delete_table('mlst_mlstdataset_moderator')

        # Deleting model 'MLSTStrain'
        db.delete_table(u'mlst_mlststrain')

        # Deleting model 'MLSTLocusNumber'
        db.delete_table(u'mlst_mlstlocusnumber')

        # Deleting model 'MLSTLocus'
        db.delete_table(u'mlst_mlstlocus')

        # Deleting model 'MLSTType'
        db.delete_table(u'mlst_mlsttype')

        # Adding model 'STType'
        db.create_table(u'mlst_sttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='type_dataset', to=orm['mlst.DataSet'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, unique=True)),
        ))
        db.send_create_signal(u'mlst', ['STType'])

        # Adding unique constraint on 'STType', fields ['dataset', 'value']
        db.create_unique(u'mlst_sttype', ['dataset_id', 'value'])

        # Adding model 'Locus'
        db.create_table(u'mlst_locus', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mlst.DataSet'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastedit_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('remote_uri', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'mlst', ['Locus'])

        # Adding model 'ExperimentData'
        db.create_table(u'mlst_experimentdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('locus', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mlst.Locus'], unique=True)),
            ('raw', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('seq', self.gf('django.db.models.fields.TextField')(default='atcg')),
            ('creat_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'mlst', ['ExperimentData'])

        # Adding model 'DataSet'
        db.create_table(u'mlst_dataset', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taxon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mlst.Taxon'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('scheme', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('creat_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastedit_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='creator', to=orm['gauth.GUser'])),
            ('remote_uri', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'mlst', ['DataSet'])

        # Adding M2M table for field moderator on 'DataSet'
        db.create_table(u'mlst_dataset_moderator', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('dataset', models.ForeignKey(orm[u'mlst.dataset'], null=False)),
            ('guser', models.ForeignKey(orm['gauth.guser'], null=False))
        ))
        db.create_unique(u'mlst_dataset_moderator', ['dataset_id', 'guser_id'])

        # Adding model 'Strain'
        db.create_table(u'mlst_strain', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taxon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mlst.Taxon'])),
            ('sttype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='strain_type', to=orm['mlst.STType'])),
            ('submittor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='submittor', to=orm['gauth.GUser'])),
            ('submit_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('strain_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('strain_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('serotype', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('serotype_formula', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('isolate_source', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=3)),
            ('isolate_year', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('isolate_country', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('cc', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('data_source', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'mlst', ['Strain'])

        # Adding M2M table for field dataset on 'Strain'
        db.create_table(u'mlst_strain_dataset', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('strain', models.ForeignKey(orm[u'mlst.strain'], null=False)),
            ('dataset', models.ForeignKey(orm[u'mlst.dataset'], null=False))
        ))
        db.create_unique(u'mlst_strain_dataset', ['strain_id', 'dataset_id'])

        # Adding model 'Taxon'
        db.create_table(u'mlst_taxon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'mlst', ['Taxon'])


    def backwards(self, orm):
        # Removing unique constraint on 'STType', fields ['dataset', 'value']
        db.delete_unique(u'mlst_sttype', ['dataset_id', 'value'])

        # Adding model 'MLSTDataSet'
        db.create_table(u'mlst_mlstdataset', (
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('lastedit_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='creator', to=orm['gauth.GUser'])),
            ('creat_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'mlst', ['MLSTDataSet'])

        # Adding M2M table for field moderator on 'MLSTDataSet'
        db.create_table(u'mlst_mlstdataset_moderator', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mlstdataset', models.ForeignKey(orm[u'mlst.mlstdataset'], null=False)),
            ('guser', models.ForeignKey(orm['gauth.guser'], null=False))
        ))
        db.create_unique(u'mlst_mlstdataset_moderator', ['mlstdataset_id', 'guser_id'])

        # Adding model 'MLSTStrain'
        db.create_table(u'mlst_mlststrain', (
            ('strain_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('cc', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('serotype', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='strain_dataset', to=orm['mlst.MLSTDataSet'])),
            ('sttype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='strain_type', to=orm['mlst.MLSTType'])),
            ('isolate_from', self.gf('django.db.models.fields.PositiveSmallIntegerField')(max_length=3)),
            ('submit_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('strain_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('submittor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='submittor', to=orm['gauth.GUser'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_source', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('isolate_year', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('isolate_country', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'mlst', ['MLSTStrain'])

        # Adding unique constraint on 'MLSTStrain', fields ['dataset', 'sttype']
        db.create_unique(u'mlst_mlststrain', ['dataset_id', 'sttype_id'])

        # Adding model 'MLSTLocusNumber'
        db.create_table(u'mlst_mlstlocusnumber', (
            ('locus', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mlst.MLSTLocus'], unique=True)),
            ('raw', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            ('seq', self.gf('django.db.models.fields.TextField')()),
            ('creat_time', self.gf('django.db.models.fields.DateTimeField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='seq_dataset', to=orm['mlst.MLSTDataSet'])),
        ))
        db.send_create_signal(u'mlst', ['MLSTLocusNumber'])

        # Adding model 'MLSTLocus'
        db.create_table(u'mlst_mlstlocus', (
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mlst.MLSTDataSet'])),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastedit_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'mlst', ['MLSTLocus'])

        # Adding model 'MLSTType'
        db.create_table(u'mlst_mlsttype', (
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='type_dataset', to=orm['mlst.MLSTDataSet'])),
        ))
        db.send_create_signal(u'mlst', ['MLSTType'])

        # Adding unique constraint on 'MLSTType', fields ['dataset', 'value']
        db.create_unique(u'mlst_mlsttype', ['dataset_id', 'value'])

        # Deleting model 'STType'
        db.delete_table(u'mlst_sttype')

        # Deleting model 'Locus'
        db.delete_table(u'mlst_locus')

        # Deleting model 'ExperimentData'
        db.delete_table(u'mlst_experimentdata')

        # Deleting model 'DataSet'
        db.delete_table(u'mlst_dataset')

        # Removing M2M table for field moderator on 'DataSet'
        db.delete_table('mlst_dataset_moderator')

        # Deleting model 'Strain'
        db.delete_table(u'mlst_strain')

        # Removing M2M table for field dataset on 'Strain'
        db.delete_table('mlst_strain_dataset')

        # Deleting model 'Taxon'
        db.delete_table(u'mlst_taxon')


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
        u'mlst.dataset': {
            'Meta': {'ordering': "['name']", 'object_name': 'DataSet'},
            'creat_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator'", 'to': "orm['gauth.GUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'lastedit_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'moderator': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'moderator'", 'symmetrical': 'False', 'to': "orm['gauth.GUser']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'remote_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'scheme': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mlst.Taxon']"})
        },
        u'mlst.experimentdata': {
            'Meta': {'ordering': "['creat_time']", 'object_name': 'ExperimentData'},
            'creat_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locus': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['mlst.Locus']", 'unique': 'True'}),
            'raw': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'seq': ('django.db.models.fields.TextField', [], {'default': "'atcg'"}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        u'mlst.locus': {
            'Meta': {'ordering': "['name']", 'object_name': 'Locus'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mlst.DataSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'lastedit_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'remote_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'mlst.strain': {
            'Meta': {'ordering': "['sttype']", 'object_name': 'Strain'},
            'cc': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'data_source': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'dataset': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'strain_dataset'", 'symmetrical': 'False', 'to': u"orm['mlst.DataSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isolate_country': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'isolate_source': ('django.db.models.fields.PositiveSmallIntegerField', [], {'max_length': '3'}),
            'isolate_year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'serotype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'serotype_formula': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'strain_id': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'strain_info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sttype': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'strain_type'", 'to': u"orm['mlst.STType']"}),
            'submit_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submittor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submittor'", 'to': "orm['gauth.GUser']"}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mlst.Taxon']"})
        },
        u'mlst.sttype': {
            'Meta': {'ordering': "['value']", 'unique_together': "(('dataset', 'value'),)", 'object_name': 'STType'},
            'dataset': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'type_dataset'", 'to': u"orm['mlst.DataSet']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'value': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'unique': 'True'})
        },
        u'mlst.taxon': {
            'Meta': {'ordering': "['name']", 'object_name': 'Taxon'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'info': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['mlst']