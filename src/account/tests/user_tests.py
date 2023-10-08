import os
import datetime

from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token


def create_user(**params):
    user=get_user_model().objects.create_user(**params)
    user.is_active=True
    user.save()
    return user

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


class PublicUserLoginTest(TestCase):    

    TOKEN_URL=reverse("account:token")
    valid_credentials_payload={
        'email' : 'test@email.com',
        'password' : 'testpassword123'
    }
    non_existing_user_payload={
        'email' : "doesnotexist@mail.com",
        'password' : 'testpassword123',
    }
    invalid_credentials_payload={
        'email' : 'test@email.com',
        'password' : 'pass'
    }
    no_password_paylad={
        'email' : 'test@email.com'
    }


    def setUp(self):
        self.user=create_user(**self.valid_credentials_payload)
        self.client = APIClient()

    def test_token_creation(self):
        response=self.client.post(
                                  self.TOKEN_URL, 
                                  self.valid_credentials_payload, 
                                  format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_token_creation_with_non_existing_user(self):
        response=self.client.post(
                                  self.TOKEN_URL, 
                                  self.non_existing_user_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_token_creation_invalid_credentials(self):
        response=self.client.post(
                                  self.TOKEN_URL, 
                                  self.invalid_credentials_payload
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)

    def test_token_creation_no_password(self):
        response=self.client.post(self.TOKEN_URL, self.no_password_paylad)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response.data)        


class PrivateUserManagementTest(TestCase):
    USER_MANAGEMENT_URL=reverse("account:account_management")

    def setUp(self):
        user_creation_payload = {
            'email': "test@gmail.com",
            'password': "testpassword123123"
        }
        image_path = os.path.join(os.path.dirname(__file__), "images", "test.jpg")
        with open(image_path, 'rb') as image_file:
            self.test_image = image_file.read()
        self.image_file = SimpleUploadedFile(
                                             "profile_image.png", 
                                             self.test_image, 
                                             content_type="image/jpeg"
        )

        self.user_update_payload = {
            'email' : "newtest@gmail.com",
            "date_of_birth": "2002-2-2",
            "profile_image": self.image_file,
        }
        self.user=create_user(**user_creation_payload)        
        self.client = APIClient()
        self.token = Token.objects.create(user=self.user)
        self.client.force_login(user=self.user)
 
    def test_valid_request(self):
        response=self.client.put(
                                 self.USER_MANAGEMENT_URL, 
                                 self.user_update_payload,
                                 HTTP_AUTHORIZATION='Token {}'.format(self.token),
                                 format='multipart',
        )
        self.assertEqual(
                         response.status_code,
                         status.HTTP_200_OK, 
                         response.data
        )
        self.user.refresh_from_db()
        
        self.assertEqual(self.user.email, self.user_update_payload["email"])
        actual_image_content = self.user.profile.pic.read()
        self.assertEqual(actual_image_content, self.test_image)
        self.assertEqual(self.user.date_of_birth, datetime.date(2002, 2, 2))

    def test_not_logged_in_user(self):
        test_client=APIClient()
        response=test_client.put(
            self.USER_MANAGEMENT_URL, 
            self.user_update_payload
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_not_allowed(self):
        response=self.client.patch(self.USER_MANAGEMENT_URL, 
                                  self.user_update_payload
                                  )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
