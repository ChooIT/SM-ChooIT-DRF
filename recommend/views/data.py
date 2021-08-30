from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from accounts.models import Tag
from accounts.serializers import TagSerializer
from recommend.models import Category, Option
from recommend.serializers import CategorySerializer, OptionSerializer


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
        queryset = Tag.objects.all()
        serializer = TagSerializer(queryset, many=True)
        return Response({
            "status": "success",
            "message": "태그 목록 조회 성공",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class OptionList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        title = request.GET.get('purpose')
        queryset = Option.objects.filter(title=title)
        serializer = OptionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
