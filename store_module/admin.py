from django.contrib import admin

# Register your models here.
from store_module.models import Product, Category, Slider, ProductImageGallery, ProductView, Comments


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name' , 'selling_price' , 'quantity' , 'status']
    prepopulated_fields = {
        'slug' : ['name']
    }

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name' , 'slug' , 'description' , 'status']
    prepopulated_fields = {
        'slug': ['name'],
    }





admin.site.register(Product , ProductAdmin)
admin.site.register(Category , CategoryAdmin)
admin.site.register(Slider)
admin.site.register(ProductImageGallery)
admin.site.register(ProductView)
admin.site.register(Comments)