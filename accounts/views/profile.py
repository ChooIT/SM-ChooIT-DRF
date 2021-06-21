from django.contrib.auth.models import update_last_login
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.views import ObtainJSONWebToken

from config.settings.authentication import JSONWebTokenAuthentication
from accounts.serializers import UserSerializer

from django.contrib.auth import get_user_model
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
@authentication_classes([JSONWebTokenAuthentication])
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
