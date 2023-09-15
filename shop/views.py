from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Article, Category, Product
from .serializers import ArticleSerializer, CategorySerializer, ProductSerializer


class CategoryAPIView(APIView):
    def get(self, *args, **kwargs):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, *args, **kwargs):
        request_data = self.request.data
        serializer = CategorySerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductAPIView(APIView):
    def get(self, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        request_data = self.request.data
        serizalizer = ProductSerializer(data=request_data)
        if serizalizer.is_valid():
            serizalizer.save()
            return Response(serizalizer.data, status=status.HTTP_201_CREATED)
        return Response(serizalizer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleAPIView(APIView):
    def get(self, *args, **kwargs):
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, *args, **kwargs):
        request_data = self.request.data
        serializer = ArticleSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
