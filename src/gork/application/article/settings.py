# -*- coding: utf-8 -*-
from django.conf import settings


ARTICLE_PER_PAGE = getattr(settings, 'ARTICLE_PER_PAGE', 10)
