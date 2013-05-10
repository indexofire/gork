# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'STType', fields ['dataset', 'value']
        db.delete_unique(u'mlst_sttype', ['dataset_id', 'value'])

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

        # Deleting model 'Taxon'
        db.delete_table(u'mlst_taxon')


    def backwards(self, orm):
        # Adding model 'STType'
        db.create_table(u'mlst_sttype', (
            ('locus_data', self.gf('django.db.models.fields.TextField')(blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, unique=True)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(related_name='type_dataset', to=orm['mlst.DataSet'])),
        ))
        db.send_create_signal(u'mlst', ['STType'])

        # Adding unique constraint on 'STType', fields ['dataset', 'value']
        db.create_unique(u'mlst_sttype', ['dataset_id', 'value'])

        # Adding model 'Locus'
        db.create_table(u'mlst_locus', (
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('lastedit_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('remote_uri', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dataset', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mlst.DataSet'])),
        ))
        db.send_create_signal(u'mlst', ['Locus'])

        # Adding model 'ExperimentData'
        db.create_table(u'mlst_experimentdata', (
            ('seq', self.gf('django.db.models.fields.TextField')(default='atcg')),
            ('creat_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('value', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('locus', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['mlst.Locus'], unique=True)),
            ('raw', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'mlst', ['ExperimentData'])

        # Adding model 'DataSet'
        db.create_table(u'mlst_dataset', (
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='creator', to=orm['gauth.GUser'])),
            ('creat_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('remote_uri', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('taxon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mlst.Taxon'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lastedit_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('scheme', self.gf('django.db.models.fields.TextField')(blank=True)),
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
            ('strain_info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('cc', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('serotype', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('data_source', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('submit_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('strain_id', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('submittor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='submittor', to=orm['gauth.GUser'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('isolate_source', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, max_length=3)),
            ('sttype', self.gf('django.db.models.fields.related.ForeignKey')(related_name='strain_type', to=orm['mlst.STType'])),
            ('taxon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mlst.Taxon'])),
            ('isolate_year', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('serotype_formula', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('isolate_country', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
        ))
        db.send_create_signal(u'mlst', ['Strain'])

        # Adding model 'Taxon'
        db.create_table(u'mlst_taxon', (
            ('info', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'mlst', ['Taxon'])


    models = {
        
    }

    complete_apps = ['mlst']