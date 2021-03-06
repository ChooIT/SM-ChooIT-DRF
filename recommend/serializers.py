from rest_framework import serializers

from accounts.models import Tag
from accounts.serializers import TagSerializer
from recommend.models import Product, Favorite, Review, ReviewImage, SearchLog, ProductTag, Category, ProductImage, \
    Estimate, Option, ProductTextCloud
from django.contrib.auth import get_user_model
User = get_user_model()


class ProductTextCloudSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTextCloud
        fields = [
            'cloud_image',
            'type',
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            'img_no',
            'prod_img_path',
            'prod_is_thumbnail'
        ]


class ProductTagSerializer(serializers.ModelSerializer):
    tag = TagSerializer(read_only=True)

    class Meta:
        model = ProductTag
        fields = [
            'tag'
        ]


class ProductSerializer(serializers.ModelSerializer):
    prod_tags = ProductTagSerializer(many=True, read_only=True)
    prod_category = serializers.StringRelatedField()
    prod_images = ProductImageSerializer(many=True, read_only=True)
    prod_text_clouds = ProductTextCloudSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'prod_no',
            'prod_name',
            'prod_manufacturer',
            'prod_category',
            'prod_price',
            'prod_preference',
            'prod_images',
            'prod_text_clouds',
            'created_at',
            'updated_at',
            'prod_tags'
        ]


class ProductThumbnailSerializer(serializers.ModelSerializer):
    prod_thumbnail = serializers.SerializerMethodField()
    prod_category = serializers.StringRelatedField()
    prod_tags = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'prod_no',
            'prod_name',
            'prod_category',
            'prod_price',
            'prod_thumbnail',
            'prod_tags'
        ]

    def get_prod_tags(self, obj):
        return ProductTag.objects.filter(prod__prod_no=obj.prod_no).values_list('tag__tag_text', flat=True)[:3]

    def get_prod_thumbnail(self, obj):
        try:
            return ProductImage.objects.get(prod_no=obj.prod_no, prod_is_thumbnail=True).prod_img_path.url
        except ProductImage.DoesNotExist:
            return None


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
            'img_no',
            'img_path',
        ]


class ReviewUserSerializer(serializers.ModelSerializer):
    tags = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'nickname',
            'emoji',
            'tags'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    review_img_thumbnail = serializers.PrimaryKeyRelatedField(queryset=ReviewImage.objects.all(), write_only=True, required=True)
    thumbnail_detail = ReviewImageSerializer(source='review_img_thumbnail', read_only=True)
    review_tags = serializers.StringRelatedField(read_only=True, many=True)
    user_no = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    user = ReviewUserSerializer(source='user_no', read_only=True)

    def create(self, validated_data):
        return Review.objects.create(**validated_data)

    class Meta:
        model = Review
        fields = [
            'review_no',
            'user',
            'user_no',
            'prod_no',
            'review_title',
            'review_text',
            'func1_rate',
            'func2_rate',
            'func3_rate',
            'review_img_thumbnail',
            'thumbnail_detail',
            'review_tags',
            'created_at',
            'updated_at'
        ]


class SearchLogSerializer(serializers.ModelSerializer):
    prod = ProductThumbnailSerializer(read_only=True)

    class Meta:
        model = SearchLog
        fields = [
            'user',
            'prod',
            'created_at'
        ]


class FavoriteSerializer(serializers.ModelSerializer):
    fav_prod = ProductThumbnailSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = [
            'fav_user',
            'fav_prod',
            'fav_created_at'
        ]


class EstimateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estimate
        fields = [
            'user',
            'prod',
            'estimate_rate'
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('__all__')


class OptionSerializer(serializers.ModelSerializer):
    title = serializers.CharField(write_only=True)
    tag = serializers.StringRelatedField()
    flag = serializers.BooleanField(read_only=True)

    class Meta:
        model = Option
        fields = [
            'title',
            'tag',
            'flag',
            'description'
        ]
