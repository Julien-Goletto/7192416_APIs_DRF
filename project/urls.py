from django.contrib import admin
from django.urls import path, include

from shop.views import ArticleAPIView, CategoryAPIView, ProductAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/article", ArticleAPIView.as_view()),
    path("api/category", CategoryAPIView.as_view()),
    path("api/product", ProductAPIView.as_view()),
]
