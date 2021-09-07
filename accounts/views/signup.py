from accounts.utils import get_nickname

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer, CreateUserTagSerializer
User = get_user_model()


@api_view(['GET'])
@permission_classes([AllowAny])
def is_registered_email(request):
    email = request.GET.get('email')
    try:
        user = User.objects.get(email=email)
        return Response({
            "message": "True",
            "active level": user.is_active
        }, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"message": "False"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    """
    {
        "email": "test@test.com",
        "password": "password",
        "gender": "m",
        "type": "i"
    }
    """
    data = request.data
    data['emoji'], data['nickname'] = get_nickname()
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "message": "회원가입에 성공하였습니다.",
            "data": {
                "email": data['email'],
                "nickname": data['nickname'],
                "emoji": data['emoji']
            }
        }, status=status.HTTP_201_CREATED)
    return Response({
        "status": "fail",
        "message": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


def upgrade_active_level(user_email):
    try:
        user = User.objects.get(email=user_email)
        user.is_active = 't'
        user.save()
        return user.active_level, True
    except User.DoesNotExist:
        return None, False


@api_view(['POST'])
@permission_classes([AllowAny])
def create_new_favorite_tag(request):
    """
    [
        {
            "user": "test@test.com",
            "tag": 1
        },
        {
            "user": "test@test.com",
            "tag": 2
        },
        ...
    ]
    """
    serializer = CreateUserTagSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        upgrade_active_level(user_email=request.data.get("user"))
        return Response({
            "status": "success",
            "message": "성공적으로 선호 태그를 등록했습니다."
        }, status=status.HTTP_201_CREATED)

    return Response({
        "status": "fail",
        "message": "태그 등록에 실패했습니다.",
        "data": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_using_prod_history(request):
    # 사용해본 제품 추가하면 회원가입 완료 로직
    level, is_user = upgrade_active_level(request.data.get('email'))
    if is_user:
        return Response({
            "status": "success",
            "message": "회원가입 완료"
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "fail",
            "message": "제품 등록 실패"
        }, status=status.HTTP_400_BAD_REQUEST)
