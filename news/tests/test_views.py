from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from news.models import Topic, Newspaper


class IndexViewTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass")
        self.client.force_login(self.user)

    def test_index_view(self) -> None:
        response = self.client.get(reverse("news:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/index.html")
        self.assertContains(response, "Newspaper Agency")


class RedactorListViewTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(self.user)

    def test_redactor_list_view(self) -> None:
        response = self.client.get(reverse("news:redactor-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/redactor_list.html")
        self.assertContains(response, "Search by username")


class NewspaperListViewTests(TestCase):

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            username="testuser", password="testpass"
        )
        self.client.force_login(self.user)
        topic = Topic.objects.create(name="Test Topic")
        Newspaper.objects.create(
            title="Test Newspaper",
            content="Test content",
            published_date="2024-05-18",
            topic=topic
        )

    def test_newspaper_list_view(self) -> None:
        response = self.client.get(reverse("news:newspaper-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/newspaper_list.html")
        self.assertContains(response, "Search by title")
        self.assertContains(response, "Test Newspaper")
