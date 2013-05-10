# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return


@login_required
def
