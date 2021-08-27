
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from config.permissions import MethodDependPermission
from recommend.models import Product, SearchLog, Favorite
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
@permission_classes([MethodDependPermission])
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


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_favorite_product(request):
    if request.method == 'POST':
        request.data['fav_user'] = request.user.id
        serializer = CreateFavoriteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "나의 찜에 성공적으로 저장했습니다."
            }, status=status.HTTP_201_CREATED)
    if request.method == 'DELETE':
        try:
            favorite = Favorite.objects.get(fav_user=request.user, fav_prod_id=request.data.get('fav_prod'))
            favorite.delete()
            return Response({
                "status": "success",
                "message": "성공적으로 찜에서 삭제했습니다."
            }, status=status.HTTP_204_NO_CONTENT)
        except Favorite.DoesNotExist:
            return Response({
                "status": "fail",
                "message": "해당 제품이 찜에 존재하지 않습니다."
            }, status=status.HTTP_204_NO_CONTENT)
