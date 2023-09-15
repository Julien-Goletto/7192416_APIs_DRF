from rest_framework.serializers import ModelSerializer

from .models import Article, Category, Product


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "name",
            "description",
            "price",
            "active",
            "date_created",
            "date_updated",
        ]


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "active", "date_created", "date_updated"]


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "active",
            "date_created",
            "date_updated",
        ]
