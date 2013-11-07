# -*- coding: utf-8 -*-
from django import forms
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, get_list_or_404
from mlst.models import *


class GeneCharField(forms.CharField):
    def __init__(self, *args, **kwargs):
        super(GeneCharField, self).__init__(args, kwargs)

    def clean(self, value):
        super(GeneCharField, self).clean(value)

        return value


class AddStrainForm(forms.Form):
    def __init__(self, slug, *args, **kwargs):
        super(AddStrainForm, self).__init__(args, kwargs)

        d = get_object_or_404(DataSet, slug=slug)
        loci = get_list_or_404(Locus, dataset=d)

        self.fields['starin_id'] = forms.CharField()

        for locus in loci:
            self.fields[locus.name] = forms.CharField(
                widget=forms.widgets.Textarea(),
            )


@login_required
def add_strain(request, slug):
    #d = DataSet.objects.get(slug=slug).taxon
    #Taxon.objects.get(slug__)
    if request.method == 'POST':
        form = AddStrainForm()
        if form.is_valid():
            strain = Strain.objects.create(
                taxon=DataSet.objects.get(slug=slug).taxon,
                sttype=check_sttype(loci),
            )
            pass

        else:
            return HttpResponse()
    else:
        form = AddStrainForm(slug)
        return "mlst/mlst_add_strain.html", {'form': form}
        #print form


@login_required
def mlst_index(request):
    tpl = 'mlst/mlst_index.html'
    ctx = {}
    ctx["taxon"] = Taxon.objects.all()
    return tpl, ctx


@login_required
def taxon_detail(request, slug):
    tpl = 'mlst/mlst_taxon_detail.html'
    ctx = {}
    return tpl, ctx
