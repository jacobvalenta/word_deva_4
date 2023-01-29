from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve

from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, RequestsClient

class AuthenticationTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test_username",
                                        password="test_password")

    def test_login(self):
        """Test JWT authentication"""
        factory = APIRequestFactory()
        
        login_url = reverse('token_obtain_pair')
        view = resolve(login_url).func.view_class

        request = factory.post(login_url, {'username': 'test_username',
                                           'password': 'test_password'},
                               format="json")
        response = view.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)