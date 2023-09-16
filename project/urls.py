from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from shop.views import ArticleViewSet, CategoryViewSet, ProductViewSet, AdminCategoryViewSet, AdminArticleViewSet

# Creating a router
router = routers.SimpleRouter()
# Then register urls, associated viewsets and base_name
router.register('category', CategoryViewSet, basename='category')
router.register('admin/category', AdminCategoryViewSet, basename='admin-category')
router.register('article', ArticleViewSet, basename='article')
router.register('admin/article', AdminArticleViewSet, basename='admin-article')
router.register('product', ProductViewSet, basename='product')

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path('api/', include(router.urls)) # Adding the router registered urls in accepted patterns
]
