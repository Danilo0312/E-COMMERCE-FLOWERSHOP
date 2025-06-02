from django.contrib import admin

from .models import Category, Product, Account, Reviews, Like, Dislike


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    exclude = ("search_vector",)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    exclude = ('password',)


admin.site.register(Reviews)
admin.site.register(Like)
admin.site.register(Dislike)

