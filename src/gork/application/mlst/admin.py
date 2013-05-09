# -*- coding: utf-8 -*-
from django.contrib import admin
from mlst.models import *


class MLSTDataSetAdmin(admin.ModelAdmin):
    pass


class MLSTTypeAdmin(admin.ModelAdmin):
    pass


class MLSTStrainAdmin(admin.ModelAdmin):
    pass


class MLSTLocusAdmin(admin.ModelAdmin):
    pass


class MLSTLocusNumberAdmin(admin.ModelAdmin):
    pass


admin.site.register(MLSTDataSet, MLSTDataSetAdmin)
admin.site.register(MLSTType, MLSTTypeAdmin)
admin.site.register(MLSTStrain, MLSTStrainAdmin)
admin.site.register(MLSTLocus, MLSTLocusAdmin)
admin.site.register(MLSTLocusNumber, MLSTLocusNumberAdmin)
