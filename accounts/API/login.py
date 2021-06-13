from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from rest_framework_jwt.views import ObtainJSONWebToken


class LoginView(ObtainJSONWebToken):
    def post(self, request):
        try:
            email = request.data.get('email')
            user = User.objects.get(email=email)
            if user.is_active < 2:
                return Response({
                    "status": "fail",
                    "message": "아직 회원가입 단계를 모두 거치지 않았습니다."
                }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                "status": "fail",
                "message": "회원가입 하지 않은 회원입니다."
            }, status=status.HTTP_400_BAD_REQUEST)

        response = super().post(request, content_type='application/json')
        if response.status_code != 200:
            return Response({
                "status": "fail",
                "message": "JWT Token 이 생성되지 않습니다."
            }, status=status.HTTP_400_BAD_REQUEST)
        return Response({
            "status": "success",
            "message": "성공적으로 로그인하였습니다.",
            "data": {
                "token": response.data['token']
            }
        })
