from accounts.utils import get_nickname

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth import get_user_model
from accounts.serializers import CreateUserSerializer, CreateUserTagSerializer
User = get_user_model()


@api_view(['GET'])
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
def create_user(request):
    """
    {
        "email": "test@test.com",
        "password": "password",
        "username": "한지용",
        "gender": "m",
        "nickname": "황제",
        "type": "i"
    }
    """
    data = request.data
    data['emoji'], data['nickname'] = get_nickname()
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "message": "회원가입에 성공하였습니다.",
            "data": {
                "nickname": data['nickname'],
                "emoji": data['emoji']
            }
        }, status=status.HTTP_201_CREATED)


def upgrade_active_level(user_email):
    try:
        user = User.objects.get(email=user_email)
        user.active_level += 1
        user.save()
        return user.active_level, True
    except User.DoesNotExist:
        return None, False


@api_view(['POST'])
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
    serializer = CreateUserTagSerializer(data=request.data, many=True)
    if serializer.is_valid():
        serializer.save()
        upgrade_active_level(user_email=request.data[0].get("user"))
        return Response({
            "status": "success",
            "message": "성공적으로 선호 태그를 등록했습니다."
        }, status=status.HTTP_201_CREATED)

    return Response({
        "status": "fail",
        "message": "태그 등록에 실패했습니다."
    }, status=status.HTTP_400_BAD_REQUEST)
