from rest_framework.reverse import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory, RequestsClient

from rest_framework_simplejwt.views import (TokenObtainPairView)

class AuthenticationTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="test_username", password="test_password")
        print(user, 'Created')

    def test_login(self):
        """Test authentication"""
        factory = APIRequestFactory()
        login_url = reverse('token_obtain_pair')
        request = factory.post(login_url, {'username': 'test_username',
                                           'password': 'test_password'},
                               format="json")
        response = TokenObtainPairView.as_view()(request)

        print(response.status_code)
        print(response.data)