# -*- coding: utf-8 -*-
from django.db import models
from captcha.fields import CaptchaField
from gform.models import Form


class FormCreateForm(models.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Form
