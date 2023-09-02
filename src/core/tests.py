from django.test import TestCase
from django.contrib.auth import get_user_model
# Create your tests here.


class UserTestCase(TestCase):

    def setUp(self):
        email="user@gmail.com"
        password="pass"
        self.user = get_user_model().objects.create_user(
            email=email,
            password=password,
            national_code=None,
            date_of_birth=None
        )

    def test_user_credentials(self):
        self.assertEqual(self.user.email, "user@gmail.com")
        self.assertTrue(self.user.check_password("pass"))
