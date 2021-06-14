from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response

from config.settings.authentication import JSONWebTokenAuthentication
from recommend.models import Product, SearchLog
from recommend.serializers import ProductSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


def create_search_log(user_id: int, prod: Product):
    try:
        user = User.objects.get(id=user_id)
        SearchLog.objects.create(user=user, prod=prod)
    except User.DoesNotExist:
        pass


class ProductViewset(viewsets.ViewSet):
    def list(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product)
        create_search_log(user_id=request.user.id, prod=product)
        return Response(serializer.data, status=status.HTTP_200_OK)
