# -*- coding: utf-8 -*-
from celery import task
from entrez.utils import get_current_date, fetch_queryset
from entrez.models import EntrezTerm


@task()
def fetch_entry(**kwargs):
    """
    Task for fetch entrez.
    """
    queryset = EntrezTerm.objects.filter(search_period=kwargs["period"]).select_related()

    if queryset:
        fetch_queryset(queryset)


@task()
def entrez_task(**kwargs):
    """
    Task for fetch entrez. Must set like {"period": n}(n is fetch days) keywords
    argument in perodictasks options in django admin.
    """
    terms = EntrezTerm.objects.filter(period=kwargs["period"],
                                      lastedit_date__lt=get_current_date()).select_related()

    for term in terms:
        if term is None:
            continue

        term.update_entry()

    terms.update(lastedit_date=get_current_date())
