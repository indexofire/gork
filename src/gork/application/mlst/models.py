# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mlst.settings import RAW_FILE_UPLOAD_TO


class MLSTDataSet(models.Model):
    name = models.CharField(max_length=255)
    info = models.TextField(blank=True)
    creat_time = models.DateTimeField(auto_now_add=True)
    lastedit_time = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator')
    moderator = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='moderator')

    class Meta:
        ordering = ['name']
        verbose_name = _('DataSet')
        verbose_name_plural = _('DataSets')

    def __unicode__(self):
        return self.name


class MLSTLocus(models.Model):
    name = models.CharField(max_length=10)
    info = models.TextField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    lastedit_time = models.DateTimeField(auto_now=True)
    dataset = models.ForeignKey(MLSTDataSet)

    class Meta:
        ordering = ['name']
        verbose_name = _('Locus')
        verbose_name_plural = _('Locus')

    def __unicode__(self):
        return '%s_%s' % (self.name, self.dataset.name)


class MLSTType(models.Model):
    dataset = models.ForeignKey(MLSTDataSet, related_name='type_dataset')
    name = models.CharField(max_length=10)
    value = models.PositiveIntegerField(default=1, unique=True)

    class Meta:
        ordering = ['value']
        verbose_name = _('ST Type')
        verbose_name_plural = _('ST Types')
        unique_together = (
            ("dataset", "value"),
        )

    def __unicode__(self):
        return self.name


class MLSTStrain(models.Model):
    STRAINS_CHOICES = (
        (1, _('Human')),
        (2, _('Animal')),
        (3, _('Food')),
        (4, _('Environment')),
        (5, _('Others')),
    )

    dataset = models.ForeignKey(MLSTDataSet, related_name='strain_dataset')
    sttype = models.ForeignKey(MLSTType, related_name='strain_type')
    submittor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='submittor')
    submit_time = models.DateTimeField(auto_now_add=True)
    strain_id = models.CharField(max_length=50)
    strain_info = models.TextField(blank=True)
    serotype = models.CharField(max_length=50)
    isolate_from = models.PositiveSmallIntegerField(
        max_length=3,
        choices=STRAINS_CHOICES,
        help_text=_('Strain isolate from human or animal, etc'),
    )
    isolate_year = models.CharField(max_length=4)
    isolate_country = models.CharField(max_length=50)
    cc = models.CharField(max_length=50)
    data_source = models.CharField(max_length=50)

    class Meta:
        ordering = ['sttype']
        verbose_name = _('Strain Info')
        verbose_name_plural = _('Strain Info')
        unique_together = (
            ("dataset", "sttype"),
        )

    def __unicode__(self):
        return self.strain_id


class MLSTLocusNumber(models.Model):
    #dataset = models.ForeignKey(MLSTDataSet, related_name='seq_dataset')
    locus = models.OneToOneField(MLSTLocus)
    value = models.PositiveIntegerField(default=1)
    seq = models.TextField(
        default='atcg',
        help_text=_('fasta format(pure text) content of nucletides'),
    )
    raw = models.FileField(upload_to=RAW_FILE_UPLOAD_TO, blank=True)
    creat_time = models.DateTimeField()

    class Meta:
        ordering = ['creat_time']
        verbose_name = _('Locus Number')
        verbose_name_plural = _('Locus Numbers')

    def __unicode__(self):
        return '%s_%s' % (self.locus.name, self.locus.value)
