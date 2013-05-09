# -*- coding: utf-8 -*-
from django.conf import settings


RAW_FILE_UPLOAD_TO = getattr(settings, 'RAW_FILE_UPLOAD_TO', '%smlst' % settings.MEDIA_ROOT)
