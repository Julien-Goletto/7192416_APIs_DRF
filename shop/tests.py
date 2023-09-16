from django.urls import reverse_lazy
from rest_framework.test import APITestCase

from .models import Category, Product, Article

class ShopAPITestCase(APITestCase):
  def format_datetime(self, value):
    # Helper method to format datetime the way the API handle it
    return value.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

class TestCategory(ShopAPITestCase):
  # Storing endpoint url to use it easily in each test we want
  url = reverse_lazy('category-list')

  def tests_list(self):
    # Fisrt create two fake categories, one only is active to test the filter
    fake_category_1 = Category.objects.create(name='Fake category 1', description='Fake category 1 description', active=True)
    Category.objects.create(name='Fake category 2', description='Fake category 2 description', active=False)

    reponse = self.client.get(self.url)
    self.assertEqual(reponse.status_code, 200)
    expected=[
      {
        'id': fake_category_1.pk,
        'name': fake_category_1.name,
        'description': fake_category_1.description,
        'active': fake_category_1.active,
        'date_created': self.format_datetime(fake_category_1.date_created),
        'date_updated': self.format_datetime(fake_category_1.date_updated),
      }
    ]
    self.assertEqual(reponse.data, expected)

  def test_create(self):
    # Check no category exists before creating one
    self.assertFalse(Category.objects.exists())
    response = self.client.post(self.url, data={"name": "New fake category"})
    # Response should be 405 because post requests are not allowed for now on
    self.assertEqual(response.status_code, 405)
    # Check no category has been created
    self.assertFalse(Category.objects.exists())

class TestProduct(ShopAPITestCase):
  url = reverse_lazy('product-list')

  def test_list(self):
    # Create first a category to link the product to
    fake_category = Category.objects.create(name='Fake category', description='Fake category description', active=True)
    fake_product_1 = Product.objects.create(name='Fake product 1', description='Fake product 1 description', category=fake_category, active=True)
    Product.objects.create(name='Fake product 2', description='Fake product 2 description', category=fake_category, active=False)
    response = self.client.get(self.url)
    self.assertEqual(response.status_code, 200)
    expected = [
      {
        'id': fake_product_1.pk,
        'name': fake_product_1.name,
        'description': fake_product_1.description,
        'category': fake_product_1.category.pk,
        'active': fake_product_1.active,
        'date_created': self.format_datetime(fake_product_1.date_created),
        'date_updated': self.format_datetime(fake_product_1.date_updated),
      }
    ]
    self.assertEqual(response.data, expected)

  def test_create(self):
    self.assertFalse(Product.objects.exists())
    response = self.client.post(self.url, data={"name": "New fake product"})
    self.assertEqual(response.status_code, 405)
    self.assertFalse(Product.objects.exists())

  def test_delete(self):
    fake_category = Category.objects.create(name='Fake category', description='Fake category description', active=True)
    fake_product = Product.objects.create(name='Fake product 2', description='Fake product 2 description', category=fake_category, active=True)
    product_count = Product.objects.count()
    response = self.client.delete(self.url, kwargs={'pk': fake_product.pk})
    self.assertEqual(response.status_code, 405)
    self.assertEqual(Product.objects.count(), product_count)
  
  def test_category_filter(self):
    fake_category_1 = Category.objects.create(name='Fake category', description='Fake category description', active=True)
    fake_category_2 = Category.objects.create(name='Fake category 2', description='Fake category 2 description', active=True)
    fake_product_1 = Product.objects.create(name='Fake product 2', description='Fake product 2 description', category=fake_category_1, active=True)
    Product.objects.create(name='Fake product 2', description='Fake product 2 description', category=fake_category_2, active=True)
    expected = [
      {
        'id': fake_product_1.pk,
        'name': fake_product_1.name,
        'description': fake_product_1.description,
        'category': fake_product_1.category.pk,
        'active': fake_product_1.active,
        'date_created': self.format_datetime(fake_product_1.date_created),
        'date_updated': self.format_datetime(fake_product_1.date_updated),
      }
    ]
    response = self.client.get(self.url + f"?category_id={fake_category_1.pk}")
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, expected)