from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from recommend.serializers import ImageSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def post_review_image(request):
    request.data['user_no'] = request.user.id
    serializer = ImageSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "status": "success",
            "message": "이미지 등록 성공",
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response({
        "status": "fail",
        "message": "이미지 등록 실패",
        "data": serializer.errors
    }, status=status.HTTP_400_BAD_REQUEST)
