from rest_framework import serializers
from recommend.models import Product, Favorite, Review, ReviewImage, Image, SearchLog, ProductTag, Category, ProductImage
from django.contrib.auth import get_user_model
User = get_user_model()


class ImageSerializer(serializers.ModelSerializer):
    img_path = serializers.ImageField(use_url=True)

    class Meta:
        model = Image
        fields = [
            'img_no',
            'img_path',
            'user_no'
        ]


class ProductTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTag
        fields = [
            'prod',
            'tag'
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    prod_img_no = ImageSerializer()

    class Meta:
        model = ProductImage
        fields = [
            'prod_img_no'
        ]


class ProductSerializer(serializers.ModelSerializer):
    prod_tags = serializers.StringRelatedField(many=True, read_only=True)
    prod_category = serializers.StringRelatedField()
    prod_images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'prod_no',
            'prod_name',
            'prod_manufacturer',
            'prod_category',
            'prod_price',
            'prod_images',
            'created_at',
            'updated_at',
            'prod_tags'
        ]


class CreateFavoriteSerializer(serializers.ModelSerializer):
    fav_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    fav_prod = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Favorite
        fields = ['fav_user', 'fav_prod', 'fav_created_at']


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = [
            "review_img_no",
            "review_is_thumbnail",
        ]


class ReviewSerializer(serializers.ModelSerializer):
    review_images = ReviewImageSerializer(many=True, read_only=True)
    review_tags = serializers.StringRelatedField(read_only=True, many=True)

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    class Meta:
        model = Review
        fields = [
            'review_no',
            'user_no',
            'prod_no',
            'review_title',
            'review_text',
            'func1_rate',
            'func2_rate',
            'func3_rate',
            'review_images',
            'review_tags',
            'created_at',
            'updated_at'
        ]


class SearchLogSerializer(serializers.ModelSerializer):
    prod = ProductSerializer(read_only=True)

    class Meta:
        model = SearchLog
        fields = [
            'user',
            'prod',
            'created_at'
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    prod = ProductSerializer(read_only=True)

    class Meta:
        model = SearchLog
        fields = [
            'user',
            'prod',
            'created_at'
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')
