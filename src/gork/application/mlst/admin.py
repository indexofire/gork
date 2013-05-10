# -*- coding: utf-8 -*-
from django.contrib import admin
from mlst.models import *


class TaxonAdmin(admin.ModelAdmin):
    pass


class DataSetAdmin(admin.ModelAdmin):
    pass


class STTypeAdmin(admin.ModelAdmin):
    pass


class StrainAdmin(admin.ModelAdmin):
    pass


class LocusAdmin(admin.ModelAdmin):
    pass


class ExperimentDataAdmin(admin.ModelAdmin):
    pass


admin.site.register(Taxon, TaxonAdmin)
admin.site.register(DataSet, DataSetAdmin)
admin.site.register(STType, STTypeAdmin)
admin.site.register(Strain, StrainAdmin)
admin.site.register(Locus, LocusAdmin)
admin.site.register(ExperimentData, ExperimentDataAdmin)
