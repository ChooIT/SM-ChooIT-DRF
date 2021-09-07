import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import Tag
from accounts.serializers import TagSerializer
from recommend.models import Category, Option
from recommend.serializers import CategorySerializer, OptionSerializer
from recommend.views.recommend.recommend_based_on_tag import make_rec


class CategoryList(APIView):
    def get(self, request):
        queryset = Category.objects.all()
        serializer = CategorySerializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "카테고리 목록 조회 성공",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class TagList(APIView):
    def get(self, request):
        queryset = Tag.objects.all()[1:12]
        serializer = TagSerializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "태그 목록 조회 성공",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class OptionList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        title = request.GET.get('cases')
        category = request.GET.get('category')
        classifications = Option.objects.all().filter(title=title, category=category) \
            .order_by('classification') \
            .distinct() \
            .values('classification')
        data = []
        for item in classifications:
            data_dict = {}
            classification = item.get('classification')
            queryset = Option.objects.filter(title=title, classification=classification, category=category)
            options = OptionSerializer(queryset, many=True)
            data_dict['classification'] = classification
            data_dict['options'] = options.data
            data.append(data_dict)
        response = {'data': data}
        return Response(response, status=status.HTTP_200_OK)


class FileList(APIView):
    def get(self, request):
        make_rec()
        return Response({
            "status": "성공"
        }, status=status.HTTP_200_OK)
