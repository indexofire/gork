# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _
from feincms.extensions import ExtensionsMixin
from mlst.settings import RAW_FILE_UPLOAD_TO


class Taxon(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    info = models.TextField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('Taxon')
        verbose_name_plural = _('Taxon')

    def __unicode__(self):
        return self.name


class DataSet(models.Model):
    taxon = models.ForeignKey(Taxon)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    info = models.TextField(blank=True)
    scheme = models.TextField(blank=True)
    creat_time = models.DateTimeField(auto_now_add=True)
    lastedit_time = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='creator')
    moderator = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='moderator')
    remote_uri = models.URLField(blank=True)

    class Meta:
        ordering = ['name']
        verbose_name = _('DataSet')
        verbose_name_plural = _('DataSet')

    def __unicode__(self):
        return "%s_%s" % (self.taxon, self.name)


class Locus(models.Model):
    LOCUS_STATUS = (
        (True, _('active')),
        (False, _('inactive')),
    )
    dataset = models.ForeignKey(DataSet)
    name = models.CharField(max_length=10)
    info = models.TextField(blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    lastedit_time = models.DateTimeField(auto_now=True)

    # set remote uri if dataset scheme is from internet.
    remote_uri = models.URLField(blank=True)

    # set the locus status if scheme changed.
    status = models.BooleanField(default=True, choices=LOCUS_STATUS)

    class Meta:
        ordering = ['name']
        verbose_name = _('Locus')
        verbose_name_plural = _('Locus')

    def __unicode__(self):
        return self.name


class STType(models.Model):
    dataset = models.ForeignKey(DataSet, related_name='type_dataset')
    value = models.PositiveIntegerField(default=1, unique=True)
    locus_data = models.TextField(blank=True)
    creat_time = models.DateTimeField(auto_now_add=True)
    lastedit_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['value']
        verbose_name = _('ST Type')
        verbose_name_plural = _('ST Type')
        unique_together = (
            ("dataset", "value"),
        )

    def __unicode__(self):
        return '%s' % self.value


class Strain(models.Model, ExtensionsMixin):
    STRAINS_CHOICES = (
        (0, _('Unknown')),
        (1, _('Human')),
        (2, _('Animal')),
        (3, _('Food')),
        (4, _('Environment')),
        (5, _('Others')),
    )

    taxon = models.ForeignKey(Taxon)
    # if there is more than one dataset for one kind of strain.
    #dataset = models.ManyToManyField(DataSet, related_name='strain_dataset')

    # same as upper
    sttype = models.ForeignKey(STType, related_name='strain_type')

    # information of submittor
    submittor = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='submittor')

    # strain create time.
    submit_time = models.DateTimeField(auto_now_add=True)

    # each strain should be only one id named.
    strain_id = models.CharField(max_length=50)

    # background information about this strain.
    strain_info = models.TextField(blank=True)

    # most kind of strain will afford a serotype for analysing.
    serotype = models.CharField(max_length=50, blank=True)

    # serotype formula
    serotype_formula = models.CharField(max_length=50, blank=True)

    # type of isolate source
    isolate_source = models.PositiveSmallIntegerField(
        default=0,
        max_length=3,
        choices=STRAINS_CHOICES,
        help_text=_('Strain isolate from human or animal, etc'),
    )

    # isolate time information
    isolate_year = models.CharField(max_length=4, blank=True)

    # isolate geo information
    isolate_country = models.CharField(max_length=50, blank=True)

    # most of isolates will be assign to a clone complex.
    cc = models.CharField(max_length=50, blank=True)

    # data from other mlst database or local upload.
    data_source = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['sttype']
        verbose_name = _('Strain Info')
        verbose_name_plural = _('Strain Info')

    def __unicode__(self):
        return self.strain_id


class ExperimentData(models.Model):
    locus = models.OneToOneField(Locus)
    raw = models.FileField(upload_to=RAW_FILE_UPLOAD_TO, blank=True)
    value = models.PositiveIntegerField(default=1, unique=True)
    sttype = models.ManyToManyField(STType)
    sequence = models.TextField(
        blank=True,
        help_text=_('fasta format content of loci nucletides'),
        unique=True,
    )
    creat_time = models.DateTimeField(auto_now_add=True)
    lastedit_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['creat_time']
        verbose_name = _('Experiment Data')
        verbose_name_plural = _('Experiment Data')

    def __unicode__(self):
        return '%s_%s' % (self.locus.name, self.value)
