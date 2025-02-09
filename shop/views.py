from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Article, Category, Product
from .serializers import ArticleSerializer, CategoryListSerializer, CategoryDetailSerializer, ProductListSerializer, ProductDetailSerializer

class MultipleSerializersMixin():
    def get_serializer_class(self):
        # If retrieve is asked, return its specific serializer
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

class ArticleViewSet(MultipleSerializersMixin, ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get("product_id")
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset
    
class CategoryViewSet(MultipleSerializersMixin, ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    # Defining a detail serializer class for the retrieve action
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)
    
    def get_serializer_class(self):
        # If retrieve is asked, return its specific serializer
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        # Action defined for POST method only
        # Usable only with a detail view
        self.get_object().disable()
        return Response()
    
class ProductViewSet(MultipleSerializersMixin, ReadOnlyModelViewSet):
    serializer_class = ProductListSerializer
    detail_serializer_class = ProductDetailSerializer

    def get_queryset(self):
        queryset = Product.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')
        if category_id is not None:
            queryset = queryset.filter(category_id=category_id)
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()
    
    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()

class AdminCategoryViewSet(MultipleSerializersMixin, ModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.all()

class AdminArticleViewSet(MultipleSerializersMixin, ModelViewSet):
    serializer_class = ArticleSerializer
    detail_serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.all()