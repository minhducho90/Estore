from django.contrib import admin
from . import models


# admin.site.register(models.Category)
@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
    ordering = ['name']
    list_display = ['name', 'slug']


@admin.register(models.SubCategory)
class SubcategoryAdmin(admin.ModelAdmin):
    autocomplete_fields = ['category']
    prepopulated_fields = {
        'slug': ['name']
    }
    list_display = ['name', 'slug', 'category_name']
    search_fields = ['name']

    def category_name(self, subcategory):
        return subcategory.category.name


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['subcategory']

    list_display = ['name', 'price', 'viewed_status', 'public_day','subcategory_name']
    list_filter = ['public_day', 'subcategory']
    list_editable = ['price']
    list_per_page = 10
    search_fields = ['name__istartswith']
    # ordering = ['name', 'price', 'viewed']

    def subcategory_name(self, product):
        return product.subcategory.name

    @admin.display(ordering='viewed')
    def viewed_status(self, product):
        if product.viewed == 0:
            return 'No'
        return 'Yes'