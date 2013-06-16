# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from docs.validators import validate_isdir


class SphinxDocProject(models.Model):
    """
    Represents a Sphinx project. Each ``SphinxDocProject`` has a name,
    a slug and a path to the root directory of a Sphinx project
    (where Sphinx’ ``conf.py``) is located).
    """
    name = models.CharField(
        max_length=100,
    )
    slug = models.SlugField(
        unique=True,
        help_text=_(u'Used in the project as its name which must be unique'),
    )
    path = models.CharField(
        max_length=255,
        validators=[validate_isdir],
        help_text=_(u'Directory which contains project conf.py file')
    )

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('sphinxdocproject-index', (), {'slug': self.slug})


class SphinxDoc(models.Model):
    """
    Represents a JSON encoded Sphinx document. The attributes ``title`` and
    ``body`` dubicate the corresponding keys in ``content`` and are used for
    the Haystack search.
    """
    project = models.ForeignKey(SphinxDocProject)
    path = models.CharField(max_length=255)
    content = models.TextField()
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)

    def __unicode__(self):
        return self.path

    @models.permalink
    def get_absolute_url(self):
        return ('sphinxdocproject-detail', (), {
            'slug': self.project.slug,
            'path': self.path, })
