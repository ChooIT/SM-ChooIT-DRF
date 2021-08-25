from random import choice

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.db.models import Count
from accounts.models import UserTag, Tag
from recommend.models import SearchLog, Product
from recommend.serializers import ProductThumbnailSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


def get_user_tags(user_id: int):
    try:
        user = User.objects.get(id=user_id)
        tags = list(UserTag.objects.filter(user=user))
        return tags, True
    except User.DoesNotExist:
        return list(Tag.objects.all()), False


def is_already_used(memo, tag):
    if tag in memo:
        return True
    memo.append(tag)
    return False


def get_tag_randomly(tag_memo, tag_list):
    while True:
        tag = choice(tag_list)
        if is_already_used(tag_memo, tag):
            continue
        return tag


@api_view(['GET'])
@permission_classes([AllowAny])
def get_item_list_of_the_day(request):
    most_searched_products = SearchLog.objects \
        .annotate(prod_count=Count('prod')) \
        .order_by('-prod_count') \
        .values_list('prod', flat=True)
    print(most_searched_products)
    products = Product.objects.all().filter(prod_no__in=most_searched_products)
    serializer = ProductThumbnailSerializer(products, many=True)
    return Response({
        "status": "success",
        "message": "오늘의 제품 리스트",
        "data": serializer.data
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def tag_filtering_product_list(request):
    tags_of_user, is_auth_user = get_user_tags(request.user.id)

    rec_based_on_tag_list = []
    tag_memo = []
    for number in range(0, 3):
        rec_dict = {}
        filter_tag = get_tag_randomly(tag_memo, tags_of_user)
        tag_text = (filter_tag.tag.tag_text if is_auth_user else filter_tag.tag_text)
        rec_dict['tag'] = tag_text

        queryset = Product.objects.filter(prod_tags__tag__tag_text=filter_tag)[:3]
        serializer = ProductThumbnailSerializer(queryset, many=True)
        rec_dict['product'] = serializer.data
        rec_based_on_tag_list.append(rec_dict)

    return Response({
        "status": "success",
        "message": "태그 기반 필터링 제품 목록 조회 성공",
        "data": rec_based_on_tag_list
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_item_list_filtered_by_category(request):
    '''
    ?category=
    ?case=
    '''
    filter_key_list = list(request.GET.keys())
    filter_dict = {}
    for filter_key in filter_key_list:
        key = {"category": "prod_category__category_name", "case": "prod_tags__tag__tag_text"}.get(filter_key)
        filter_dict[key] = request.GET.get(filter_key)
    product = Product.objects.filter(**filter_dict)
    serializer = ProductThumbnailSerializer(product, many=True)
    return Response({
        "status": "success",
        "message": "카테고리 별 상품 리스트 출력 성공",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendation_list_based_on_alike_user(request):
    # TODO: 추천 로직
    product = Product.objects.all()[:5]
    serializer = ProductThumbnailSerializer(product, many=True)

    return Response({
        "status": "success",
        "message": "나와 비슷한 유저가 좋아하는 제품 기반 추천 리스트 출력 성공",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendation_list_based_on_alike_item(request):
    # TODO: 추천 로직
    product = Product.objects.all()[:5]
    serializer = ProductThumbnailSerializer(product, many=True)

    return Response({
        "status": "success",
        "message": "내가 좋아하는 제품과 유사한 추천 리스트 출력 성공",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendation_list_based_on_mix(request):
    #  TODO: 추천 로직
    product = Product.objects.all()[:5]
    serializer = ProductThumbnailSerializer(product, many=True)

    return Response({
        "status": "success",
        "message": "종합적 추천 성공",
        "data": serializer.data
    }, status=status.HTTP_200_OK)