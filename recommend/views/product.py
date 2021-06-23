from random import choice

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from accounts.models import UserTag, Tag
from recommend.models import Product, SearchLog
from recommend.serializers import ProductSerializer, CreateFavoriteSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


def get_user_tags(user_id: int):
    try:
        user = User.objects.get(id=user_id)
        tags = list(UserTag.objects.filter(user=user))
        return tags, True
    except User.DoesNotExist:
        return list(Tag.objects.all()), False


def create_search_log(user_id: int, prod: Product):
    try:
        user = User.objects.get(id=user_id)
        SearchLog.objects.create(user=user, prod=prod)
    except User.DoesNotExist:
        pass


@api_view(['GET'])
@permission_classes([AllowAny])
def tag_filtering_product_list(request):
    tags_of_user, is_auth_user = get_user_tags(request.user.id)
    filter_tag = choice(tags_of_user)
    tag_text = (filter_tag.tag.tag_text if is_auth_user else filter_tag.tag_text)
    queryset = Product.objects.filter(prod_tags__tag__tag_text=filter_tag)
    serializer = ProductSerializer(queryset, many=True)
    return Response({
        "status": "success",
        "message": "태그 기반 필터링 제품 목록 조회 성공",
        "data": {
            "tag": tag_text,
            "product": serializer.data
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_detail(request, pk=None):
    queryset = Product.objects.all()
    product = get_object_or_404(queryset, pk=pk)
    serializer = ProductSerializer(product)
    create_search_log(user_id=request.user.id, prod=product)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user_favorite_product(request):
    request.data['fav_user'] = request.user.id
    serializer = CreateFavoriteSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "message": "나의 찜에 성공적으로 저장했습니다."
        }, status=status.HTTP_201_CREATED)
