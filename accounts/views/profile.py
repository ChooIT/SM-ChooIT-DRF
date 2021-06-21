from django.contrib.auth.models import update_last_login
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.views import ObtainJSONWebToken

from config.settings.authentication import JSONWebTokenAuthentication
from accounts.serializers import UserSerializer

from django.contrib.auth import get_user_model

from recommend.models import Review, SearchLog, Favorite
from recommend.serializers import ReviewSerializer, SearchLogSerializer, FavoriteSerializer

User = get_user_model()


class LoginView(ObtainJSONWebToken):
    def post(self, request):
        try:
            user = User.objects.get(email=request.data.get('email'))
            update_last_login(None, user)
            res = super().post(request, content_type='application/json')
            if res.status_code == 200:
                return Response({
                    "token": res.data.get('token')
                }, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile_detail(request):
    user = User.objects.get(id=request.user.id)
    user_serializer = UserSerializer(user)
    return Response({
        "status": "success",
        "message": "프로필 조회 성공",
        "data": {
            "profile": user_serializer.data,
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_search_log_list(request):
    user = User.objects.get(id=request.user.id)
    queryset = SearchLog.objects.filter(user=user)
    search_log_serializer = SearchLogSerializer(queryset, many=True)
    return Response({
        "status": "success",
        "message": "내가 본 제품 목록 조회 성공",
        "data": search_log_serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_favorite_list(request):
    user = User.objects.get(id=request.user.id)
    queryset = Favorite.objects.filter(fav_user=user)
    favorite_serializer = FavoriteSerializer(queryset, many=True)
    return Response({
        "status": "success",
        "message": "내가 찜 제품 목록 조회 성공",
        "data": favorite_serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_review_list(request):
    user = User.objects.get(id=request.user.id)
    queryset = Review.objects.filter(user_no=user)
    review_serializer = ReviewSerializer(queryset, many=True)
    return Response({
        "status": "success",
        "message": "나의 리뷰 목록 조회 성공",
        "data": review_serializer.data
    }, status=status.HTTP_200_OK)
