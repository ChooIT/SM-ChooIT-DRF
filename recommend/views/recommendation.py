from random import choice, randint

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.db.models import Count
from accounts.models import UserTag, Tag
from recommend.models import SearchLog, Product, Estimate, Option
from recommend.serializers import ProductThumbnailSerializer
from django.contrib.auth import get_user_model

from recommend.views.recommend.recommend_based_on_tag import get_recommendation_list_based_on_tag
from recommend.views.recommend.recommend_based_on_user import get_recommendation_list_based_on_user

User = get_user_model()


def get_user_tags(user_id: int):
    try:
        user = User.objects.get(id=user_id)
        tags = list(UserTag.objects.filter(user=user))
        return tags, True
    except User.DoesNotExist:
        return list(Tag.objects.all().filter(id__gt=1, id__lt=13)), False


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
    for number in range(0, 2):
        rec_dict = {}
        filter_tag = get_tag_randomly(tag_memo, tags_of_user)
        tag_text = (filter_tag.tag.tag_text if is_auth_user else filter_tag.tag_text)
        rec_dict['tag'] = tag_text

        queryset = Product.objects.filter(prod_tags__tag__tag_text=filter_tag)[:6]
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
    category = request.GET.get('category')
    cases = request.GET.getlist('cases')

    if (len(cases) == 1) and (cases[0] == '게임' or '디자인그래픽' or '문서작업' or '사무용' or '코딩' or '학생'):
        cases = Option.objects.all().filter(title=cases[0], flag=True).values_list('tag__tag_text')
    product = Product.objects.filter(prod_category__category_name=category, prod_tags__tag__tag_text__in=cases)\
        .values_list('prod_no', flat=True).distinct()
    product = Product.objects.filter(prod_no__in=product)

    serializer = ProductThumbnailSerializer(product, many=True)
    return Response({
        "status": "success",
        "message": "카테고리 별 상품 리스트 출력 성공",
        "data": serializer.data,
    }, status=status.HTTP_200_OK)


def is_estimate_exist(user_id):
    if Estimate.objects.all().filter(user_id=user_id).count() == 0:
        return False
    return True


def make_user_preference(user):
    number_of_products = Product.objects.all().count() + 1
    keys = [str(index) for index in range(1, number_of_products)]
    values = ['' for number in range(1, number_of_products)]
    user_preference_dict = dict(zip(keys, values))

    for estimate in Estimate.objects.all().filter(user=user):
        user_preference_dict[str(estimate.prod_id)] = estimate.estimate_rate
    return user_preference_dict


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendation_list_based_on_alike_user(request):
    if not is_estimate_exist(request.user.id):
        return Response({
            "status": "fail",
            "message": "제품 평가가 이루어진 후에 제품을 추천해줄 수 있어요"
        }, status=status.HTTP_400_BAD_REQUEST)

    user_preference = make_user_preference(request.user)
    recommendation_list = get_recommendation_list_based_on_user(user_preference)
    product = Product.objects.all().filter(prod_no__in=recommendation_list[0])
    serializer = ProductThumbnailSerializer(product, many=True)

    return Response({
        "status": "success",
        "message": "나와 비슷한 유저가 좋아하는 제품 기반 추천 리스트 출력 성공",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendation_list_based_on_alike_item(request):
    if not is_estimate_exist(request.user.id):
        return Response({
            "status": "fail",
            "message": "제품 평가가 이루어진 후에 제품을 추천해줄 수 있어요"
        }, status=status.HTTP_400_BAD_REQUEST)

    recommendation_list = get_recommendation_list_based_on_tag(request.user.id)
    product = Product.objects.all().filter(prod_no__in=recommendation_list)
    serializer = ProductThumbnailSerializer(product, many=True)

    return Response({
        "status": "success",
        "message": "내가 좋아하는 제품과 유사한 추천 리스트 출력 성공",
        "data": serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recommendation_list_based_on_mix(request):
    if not is_estimate_exist(request.user.id):
        return Response({
            "status": "fail",
            "message": "제품 평가가 이루어진 후에 제품을 추천해줄 수 있어요"
        }, status=status.HTTP_400_BAD_REQUEST)

    user_preference = make_user_preference(request.user)
    recommendation_list = get_recommendation_list_based_on_user(user_preference)
    prod_list = list(recommendation_list[0])
    prod_list += get_recommendation_list_based_on_tag(request.user.id)
    print(prod_list)

    mix_recommendation = []
    for number in range(5):
        index = randint(0, len(prod_list) - 1)
        mix_recommendation.append(prod_list[index])

    queryset = Product.objects.all().filter(prod_no__in=mix_recommendation)
    serializer = ProductThumbnailSerializer(queryset, many=True)

    return Response({
        "status": "success",
        "message": "종합적 추천 성공",
        "data": serializer.data
    }, status=status.HTTP_200_OK)
