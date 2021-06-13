from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status

from accounts.serializers import CreateUserSerializer


@api_view(['GET'])
def is_registered_email(request):
    email = request.GET.query_params.get('email')
    try:
        User.objects.get(email=email)
        return Response({"message": "True"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"message": "False"}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "message": "회원가입에 성공하였습니다."
        }, status=status.HTTP_201_CREATED)
