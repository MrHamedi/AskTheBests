from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
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

    def test_email_normalized(self):
        user = get_user_model().objects.create_user(email="example@GMAIL.COM" ,password='pass' )
        user.save()
        self.assertEqual(user.email, 'example@gmail.com')

    def test_credentials_superuser(self):
        email="superuser@gmail.com"
        password="pass"
        user=get_user_model().objects.create_superuser(
            email=email,
            password=password,
            national_code='123456789',
            date_of_birth=timezone.now()
        )
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

