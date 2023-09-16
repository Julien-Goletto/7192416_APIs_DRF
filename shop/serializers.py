from rest_framework.serializers import ModelSerializer, SerializerMethodField

from .models import Article, Category, Product


class ArticleSerializer(ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "name",
            "description",
            "price",
            "product",
            "active",
            "date_created",
            "date_updated",
        ]

class ProductSerializer(ModelSerializer):
    articles = SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "category",
            "articles",
            "active",
            "date_created",
            "date_updated",
        ]
    
    def get_articles(self, instance):
        queryset = instance.articles.filter(active=True)
        serializer = ArticleSerializer(queryset, many=True)
        return serializer.data

class CategorySerializer(ModelSerializer):
    # Define a proper serializer for the products field
    # Using SerializerMethodField requiers a method with the name get_<field_name>
    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "description", "active", "date_created", "date_updated", "products"]

    # Apply this method for each category instance in our category list
    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductSerializer(queryset, many=True)
        return serializer.data

