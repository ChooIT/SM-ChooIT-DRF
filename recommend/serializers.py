from rest_framework import serializers
from recommend.models import Product, Favorite, Review, ReviewImage, Image
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


class ProductSerializer(serializers.ModelSerializer):
    prod_tags = serializers.StringRelatedField(many=True, read_only=True)
    prod_category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = [
            'prod_no',
            'prod_name',
            'prod_manufacturer',
            'prod_category',
            'prod_price',
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

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    class Meta:
        model = Review
        fields = [
            'user_no',
            'prod_no',
            'review_title',
            'review_text',
            'func1_rate',
            'func2_rate',
            'func3_rate',
            'review_images',
            'created_at',
            'updated_at'
        ]
