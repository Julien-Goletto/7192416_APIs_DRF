from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Article, Category, Product
from .serializers import ArticleSerializer, CategoryListSerializer, CategoryDetailSerializer, ProductListSerializer, ProductDetailSerializer

class ViewSetMixin(ReadOnlyModelViewSet):
    def get_serializer_class(self):
        # If retrieve is asked, return its specific serializer
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()


class ArticleViewSet(ReadOnlyModelViewSet):
    serializer_class = ArticleSerializer
    def get_queryset(self):
        queryset = Article.objects.filter(active=True)
        product_id = self.request.GET.get("product_id")
        if product_id is not None:
            queryset = queryset.filter(product_id=product_id)
        return queryset
    
class CategoryViewSet(ViewSetMixin):
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
    
class ProductViewSet(ReadOnlyModelViewSet):
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

