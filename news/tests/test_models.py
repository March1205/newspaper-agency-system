from django.test import TestCase
from news.models import Topic, Redactor, Newspaper


class RedactorModelTests(TestCase):

    def test_string_representation(self) -> None:
        redactor = Redactor.objects.create(
            username="testuser", first_name="John", last_name="Doe"
        )
        self.assertEqual(str(redactor), "testuser (John Doe)")


class TopicModelTests(TestCase):

    def test_string_representation(self) -> None:
        topic = Topic.objects.create(name="Test Topic")
        self.assertEqual(str(topic), "Test Topic")


class NewspaperModelTests(TestCase):

    def test_string_representation(self) -> None:
        topic = Topic.objects.create(name="Test Topic")
        newspaper = Newspaper.objects.create(
            title="Test Newspaper",
            content="Test content",
            published_date="2024-05-18",
            topic=topic
        )
        self.assertEqual(str(newspaper), "Test Newspaper, 2024-05-18")
