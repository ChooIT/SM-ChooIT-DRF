from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from recommend.models import Review
from recommend.serializers import ImageSerializer, ReviewSerializer, ReviewImageSerializer
from recommend.utils import get_first_p_tag_value
from django.contrib.auth import get_user_model
User = get_user_model()


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


@api_view(['GET'])
@permission_classes([AllowAny])
def review_list(request):
    if request.GET.get('prod_no'):
        queryset = Review.objects.all().filter(prod_no=request.GET.get('prod_no'))
    else:
        queryset = Review.objects.all()
    for data in queryset:
        data.review_text = get_first_p_tag_value(data.review_text)
    serializer = ReviewSerializer(queryset, many=True)
    return Response({
        "status": "success",
        "message": "리뷰 리스트 조회 성공",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def review_retrieve(request, pk=None):
    queryset = Review.objects.all()
    review = get_object_or_404(queryset, pk=pk)
    serializer = ReviewSerializer(review)
    return Response(serializer.data, status=status.HTTP_200_OK)
