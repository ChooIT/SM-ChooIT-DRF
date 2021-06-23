from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from recommend.models import Review, ReviewImage, ReviewTag
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


def create_review_tags(review_no: int, tag_no_list: list) -> None:
    if len(tag_no_list) == 0:
        return
    for tag_no in tag_no_list:
        ReviewTag.objects.create(
            review_no_id=review_no,
            tag_id=tag_no
        )
    return


def create_review_image(review_no, review_img_no_list, thumbnail_no):
    if len(review_img_no_list) == 0:
        return
    for no in review_img_no_list:
        image = ReviewImage.objects.create(
            review_no_id=review_no,
            review_img_no_id=no
        )
        if no == thumbnail_no:
            image.review_is_thumbnail = True
            image.save()
    return


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_new_review(request):
    request.data['user_no'] = request.user.id
    images = request.data.pop('images')
    tags = request.data.pop('review_tags')

    serializer = ReviewSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        review_no = serializer.data.get('review_no')
    else:
        return Response({
            "status": "fail",
            "message": "리뷰 등록 실패",
            "data": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    create_review_tags(review_no, tags)
    create_review_image(review_no, images.get('review_img_no'), images.get('thumbnail'))
    return Response({
            "status": "success",
            "message": "리뷰 등록 성공",
        }, status=status.HTTP_201_CREATED)
