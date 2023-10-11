from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.utils import IntegrityError

from ..models import Question


def user_creator(email="test@mail.com", password="test_password"):
    return get_user_model().objects.create_user(email=email, password=password)


class QuestionModelTests(TestCase):

    def setUp(self):
        self.user=user_creator()
        self.now = timezone.now()
        self.question=Question.objects.create(
            title="example title",
            body="example body",
            author=self.user,
        )

    def test_question_created(self):
        self.assertEqual(Question.objects.count(), 1)

    def test_slug_creator(self):
        self.assertEqual(self.question.slug, "example-title")

    def test_questions_with_similar_titles(self):
        with self.assertRaises(IntegrityError):
            new_qustion=Question.objects.create(
                title="example title",
                body="new example body",
                author=self.user,
            )

    def test_another_authr_used_similar_title(self):
        self.user=user_creator(
                               email="newtest@mail.com", 
                               password="test_password",
        )

    def test_question_publish_time(self):
        self.assertGreaterEqual(self.question.publish, self.now)

    def test_question_update_time(self):
        before = timezone.now()
        self.question.title="changed"
        self.question.save()
        self.question.refresh_from_db()
        after = timezone.now()
        for time in before, after:
            time.replace(microsecond=0)
        self.assertTrue(before <= self.question.update <= after,f"---{self.question.update}---{self.question.publish}" )