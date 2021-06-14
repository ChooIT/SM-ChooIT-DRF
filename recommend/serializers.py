from rest_framework import serializers
from recommend.models import Product, ProductTag, Category


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
