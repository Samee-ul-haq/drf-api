from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class ProductTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='test', password='pass')
        self.client.force_authenticate(user=self.user)

    def test_product_list(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
