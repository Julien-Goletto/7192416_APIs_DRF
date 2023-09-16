from rest_framework.serializers import ModelSerializer, SerializerMethodField, ValidationError

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

    def validate_price(self, price):
        if price < 1:
            raise ValidationError("Price must be greater than 1€")
        return price

    def validate_active(self, active):
        if not active:
            raise ValidationError("Article must be active")
        return active

class ProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "active",
            "date_created",
            "date_updated",
        ]
    
class ProductDetailSerializer(ModelSerializer):
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

class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "active", "date_created", "date_updated"]

    def validate_name(self, value):
        # Early check that the categorye exists
        if Category.objects.filter(name=value).exists():
            raise ValidationError("Category already exists")
        return value
    
    def validate(self, data):
        # Check if the name is present in category description
        if data["name"] not in data["description"]:
            raise ValidationError("Name must be present in description")
        return data
    
class CategoryDetailSerializer(ModelSerializer):
    # Define a proper serializer for the products field
    # Using SerializerMethodField requiers a method with the name get_<field_name>
    products = SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "description", "active", "date_created", "date_updated", "products"]

    # Apply this method for each category instance in our category list
    def get_products(self, instance):
        queryset = instance.products.filter(active=True)
        serializer = ProductListSerializer(queryset, many=True)
        return serializer.data
