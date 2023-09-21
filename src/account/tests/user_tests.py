from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient
from rest_framework import status


def create_user(**params):
    return get_user_model().objects.createuser(**params)


class PublicUserCreationTestCase(TestCase):
    User_Creation_URL = reverse("account:create_user")

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email': "test@gmail.com",
            'password': "testpassword123123"
        }
        self.response = self.client.post(
            self.User_Creation_URL,
            self.payload,
            format='json',
        )

    def test_user_creation(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(get_user_model().objects.filter(
                        **self.response.data).exists())

    def test_creating_same_user(self):
        response = self.client.post(self.User_Creation_URL,
                                    email="test@gmail.com",
                                    password="testpassword"
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password(self):
        response = self.client.post(self.User_Creation_URL,
                                    email="test@gmail.com",
                                    password="tp"
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email(self):
        response = self.client.post(self.User_Creation_URL,
                                    email="test@ad",
                                    password="testpassword"
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
