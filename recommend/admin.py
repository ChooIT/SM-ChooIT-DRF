from django.contrib import admin
from recommend.models import Category, Image, Product, ProductImage, ProductTag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category_name',
        'created_at'
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'img_no',
        'img_path',
        'user_no'
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'prod_no',
        'prod_name',
        'prod_manufacturer',
        'prod_price',
        'created_at',
        'updated_at'
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'prod_no',
        'prod_img_no',
        'created_at',
    )


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = (
        'prod',
        'tag',
        'created_at'
    )
