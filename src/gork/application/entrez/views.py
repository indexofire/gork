# -*- coding: utf-8 -*-
from entrez.models import EntrezTerm, EntrezEntry
from entrez.forms import AddSearchForm


def index(request):
    templates = 'entrez/entrez_index.html'
    objects = EntrezEntry.objects.fileter(user=request.user).select_related()
    context = {'objects': objects}

    return templates, context


def group_list(request):
    pass


def add_search(request, keyword):
    form = AddSearchForm
    template = 'entrez/entrez_add_search.html'
    context = {}

    if request.method == 'POST':
        form = AddSearchForm(request.POST)
        if form.is_valid():
            pass

    else:
        return template, context
