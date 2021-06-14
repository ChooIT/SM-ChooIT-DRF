from rest_framework import serializers
from recommend.models import Product, ProductTag, Favorite
from django.contrib.auth import get_user_model
User = get_user_model()


class ProductTagSerializer(serializers.ModelSerializer):
    tag = serializers.StringRelatedField()

    class Meta:
        model = ProductTag
        fields = ['tag']


class ProductSerializer(serializers.ModelSerializer):
    tags = ProductTagSerializer(many=True, read_only=True)
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
            'tags'
        ]


class CreateFavoriteSerializer(serializers.ModelSerializer):
    fav_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    fav_prod = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Favorite
        fields = ['fav_user', 'fav_prod', 'fav_created_at']
