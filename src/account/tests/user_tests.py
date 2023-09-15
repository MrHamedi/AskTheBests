from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient


def create_user (**params):
    return get_user_model().objects.createuser(**params)


class PublicUserCreationTestCase(TestCase):
    User_Creation_URL = reverse("account:create_user")

    def setUp(self):
        self.client = APIClient()
        self.response = self.client.post(
                                        self.User_Creation_URL, 
                                        email="test@gmail.com", 
                                        password="testpassword"
                                        )

    def test_user_creation(self):
        self.assertEqual(self.response.status_code, 201)
        self.assertTrue(get_user_model().objects.filter(
                        **self.response.data()).exists())

    def test_creating_same_user(self):
        response = self.client.post(self.User_Creation_URL, 
                        email="test@gmail.com", 
                        password="testpassword"
                        )
        self.assertEqual(response.status_code, 409)
    
    def test_short_password(self):
        response = self.client.post(self.User_Creation_URL, 
                                    email="test@gmail.com", 
                                    password="tp"
                                    )
        self.assertEqual(response.status_code, 400)

    def test_invalid_email(self):
        response = self.client.post(self.User_Creation_URL, 
                                    email="test@ad", 
                                    password="testpassword"
                                    )       
        self.assertEqual(response.status_code, 400)