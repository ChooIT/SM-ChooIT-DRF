from django.contrib import admin
from recommend.models import Category, Product, ProductImage, ProductTag, Review, ReviewImage, ReviewTag, SearchLog, \
    Estimate, Favorite, Option, ProductTextCloud


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category_name',
        'created_at'
    )


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = [
        'option_id',
        'title',
        'category',
        'classification',
        'tag',
        'flag',
        'description',
        'created_at'
    ]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'prod_no',
        'prod_name',
        'prod_category',
        'prod_manufacturer',
        'prod_price',
        'prod_preference',
        'created_at',
        'updated_at'
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = (
        'img_no',
        'prod_no',
        'prod_img_path',
        'prod_is_thumbnail',
        'created_at'
    )


@admin.register(ProductTextCloud)
class ProductTextCloudAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'prod_no',
        'cloud_image',
        'type',
        'created_at'
    )


@admin.register(ProductTag)
class ProductTagAdmin(admin.ModelAdmin):
    list_display = (
        'prod',
        'tag',
        'created_at'
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user_no',
        'prod_no',
        'review_title',
        'review_text',
        'review_img_thumbnail',
        'func1_rate',
        'func2_rate',
        'func3_rate',
        'created_at',
        'updated_at'
    )


@admin.register(ReviewImage)
class ReviewImageAdmin(admin.ModelAdmin):
    list_display = (
        'img_no',
        'img_path',
        'user_no',
        'created_at'
    )


@admin.register(ReviewTag)
class ReviewTagAdmin(admin.ModelAdmin):
    list_display = [
        'review_no',
        'tag',
        'created_at'
    ]


@admin.register(SearchLog)
class ReviewTagAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'prod',
        'created_at'
    ]


@admin.register(Estimate)
class EstimateAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'prod',
        'estimate_rate'
    ]


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = [
        'fav_user',
        'fav_prod',
        'fav_created_at'
    ]

