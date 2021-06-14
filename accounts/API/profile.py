from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from config.settings.authentication import JSONWebTokenAuthentication
from accounts.models import UserTag
from accounts.serializers import UserSerializer, UserTagSerializer

from django.contrib.auth import get_user_model
User = get_user_model()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JSONWebTokenAuthentication])
def get_profile_detail(request):
    user = User.objects.get(id=request.user.id)
    user_serializer = UserSerializer(user)
    tag = UserTag.objects.filter(user=user)
    tag_serializer = UserTagSerializer(tag, many=True)
    return Response({
        "status": "success",
        "message": "프로필 조회 성공",
        "data": {
            "profile": user_serializer.data,
            "tag": tag_serializer.data
        }
    }, status=status.HTTP_200_OK)
