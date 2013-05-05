# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
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

    return tpl, ctx


@login_required()
def term_list(request, slug):
    tpl = 'entrez/entrez_term_list.html'
    # todo: permission to check other user's term
    term = EntrezTerm.objects.get(slug=slug)
    objects = EntrezEntry.objects.filter(term=term).select_related()
    terms = EntrezTerm.objects.filter(owner=request.user).select_related()
    form = AddTermForm()
    ctx = {
        "objects": objects[:30],
        "terms": terms,
        "form": form,
    }
    return tpl, ctx


@csrf_exempt
def add_term(request):
    #tp = 'entrez/entrez_add_term.html'
    form_class = AddTermForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            term = EntrezTerm.objects.create(
                title=form.cleaned_data["title"],
                db=form.cleaned_data["db"],
                search_period=form.cleaned_data["period"],
                owner=request.user,
                condition=form.cleaned_data["term"],
                creation_date=get_current_date(),
                lastedit_date=get_current_date(),
            )
            term.save()

    return app_reverse('entrez-index', )


@csrf_exempt
def mark_as_read(request):
    if request.method == "POST":
        entry = get_object_or_404(EntrezEntry, pk=request.POST.get('feed_item_id'))
        entry.read = True
        entry.save()

    return HttpResponse()
