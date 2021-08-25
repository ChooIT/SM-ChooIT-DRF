
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from recommend.models import Product, SearchLog
from recommend.serializers import ProductSerializer, CreateFavoriteSerializer, EstimateSerializer
from django.contrib.auth import get_user_model
User = get_user_model()


def create_search_log(user_id: int, prod: Product):
    try:
        user = User.objects.get(id=user_id)
        SearchLog.objects.create(user=user, prod=prod)
    except User.DoesNotExist:
        pass


@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def get_product_detail(request, pk=None):
    if request.method == 'GET':
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product)
        create_search_log(user_id=request.user.id, prod=product)
        return Response(serializer.data, status=status.HTTP_200_OK)
    if request.method == 'POST':
        request.data['user'] = request.user.id
        request.data['prod'] = pk
        serializer = EstimateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "성공적으로 평가를 등록했습니다.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


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
