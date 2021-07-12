from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from config.permissions import ReadOnly, IsOwnerOrReadOnly
from recommend.models import Review, ReviewImage, ReviewTag
from recommend.serializers import ReviewSerializer, ReviewImageSerializer
from recommend.utils import get_first_p_tag_value
from django.contrib.auth import get_user_model

User = get_user_model()


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def post_review_image(request):
    request.data['review_user_no'] = request.user.id
    serializer = ReviewImageSerializer(data=request.data)
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


#
# @api_view(['DELETE'])
# @permission_classes([IsAuthenticated, IsOwnedByProfile])
# def delete_review(request, pk=None):
#     try:
#         review = Review.objects.get(pk=pk)
#     except Review.DoesNotExist:
#         raise Http404
#     review.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)


class ReviewDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            obj = Review.objects.get(pk=pk)
            self.check_object_permissions(self.request, obj)
            return obj
        except Review.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        review = self.get_object(pk)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk, format=None):
        review = self.get_object(pk)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def create_review_tags(review_no: int, tag_no_list: list) -> None:
    if len(tag_no_list) == 0:
        return
    for tag_no in tag_no_list:
        ReviewTag.objects.create(
            review_no_id=review_no,
            tag_id=tag_no
        )
    return


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_new_review(request):
    request.data['user_no'] = request.user.id
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
    return Response({
        "status": "success",
        "message": "리뷰 등록 성공",
        "data": {
            "review_no": review_no
        }
    }, status=status.HTTP_201_CREATED)
