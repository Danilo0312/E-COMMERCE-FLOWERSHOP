from django.contrib import admin

from .models import ProductFeatures, FeatureValidator, CategoryFeature

admin.site.register(ProductFeatures)
admin.site.register(FeatureValidator)
admin.site.register(CategoryFeature)
