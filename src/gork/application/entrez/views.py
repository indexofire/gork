# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from feincms.content.application.models import app_reverse
from entrez.models import EntrezEntry, EntrezTerm
from entrez.forms import AddTermForm
from entrez.utils import get_current_date


def get_user_all_terms(request):
    return EntrezTerm.objects.filter(owner=request.user).select_related()


def get_user_all_entries(request):
    return EntrezEntry.objects.filter(owner=request.user).select_related()


@login_required()
def index(request):
    tpl = 'entrez/entrez_index.html'
    ctx = {}
    ctx["objects"] = get_user_all_entries(request)
    ctx["terms"] = get_user_all_terms(request)
    ctx["form"] = AddTermForm()
    ctx["ct_id"] = ContentType.objects.get_for_model(EntrezEntry).id
    return tpl, ctx


@login_required()
def term_list(request, slug):
    tpl = 'entrez/entrez_term_list.html'
    # todo: permission to check other user's term
    term = EntrezTerm.objects.get(slug=slug)
    objects = EntrezEntry.objects.filter(term=term, read=False).select_related()
    terms = EntrezTerm.objects.filter(owner=request.user).select_related()
    form = AddTermForm()
    ct_id = ContentType.objects.get_for_model(EntrezEntry).id
    ctx = {
        "objects": objects[:30],
        "terms": terms,
        "form": form,
        "term": term,
        "ct_id": ct_id,
    }
    return tpl, ctx


@csrf_exempt
def add_term(request):
    #tp = 'entrez/entrez_add_term.html'
    form_class = AddTermForm
    if request.method == 'POST':
        form = form_class(request.POST)

        #if form.is_valid():
        #    term = EntrezTerm.objects.create(
        #        name=form.cleaned_data["name"],
                #slug=form.cleaned_data["slug"],
        #        db=form.cleaned_data["db"],
        #        period=form.cleaned_data["period"],
        #        owner=request.user,
        #        term=form.cleaned_data["term"],
        #        creation_date=get_current_date(),
        #        lastedit_date=get_current_date(),
        #    )
        #    term.save()

        if form.is_valid():
            term = form.save(commit=False)
            print term.name
            term.slug = slugify(term.name)
            print term.slug
            term.creation_date = term.lastedit_date = get_current_date()
            term.owner = request.user
            term.save()

        return app_reverse('entrez-index', 'entrez.urls')

    return app_reverse('entrez-index', 'entrez.urls')


@csrf_exempt
def mark_as_read(request):
    if request.method == "POST":
        entry = get_object_or_404(EntrezEntry, pk=request.POST.get('entrezentry_id'))
        if entry.read is True:
            return HttpResponse()
        else:
            entry.read = True
            entry.save()

    return HttpResponse()


@csrf_exempt
def mark_all_as_read(request):
    if request.method == "POST":
        entries = EntrezEntry.objects.filter(owner=request.user, read=False, term=request.POST.get('term'))
        if entries:
            return HttpResponse()

        else:
            entries.update(read=True)

    return HttpResponse()
