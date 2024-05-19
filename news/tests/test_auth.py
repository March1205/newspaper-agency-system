from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

HOME_PAGE = reverse("news:index")
REDACTORS_LIST = reverse("news:redactor-list")
NEWSPAPERS_LIST = reverse("news:newspaper-list")
TOPICS_LIST = reverse("news:topic-list")


class TestsForPublicRequired(TestCase):

    def test_login(self) -> None:
        response = self.client.get(HOME_PAGE)
        self.assertNotEqual(response.status_code, 200)

    def test_driver_list(self):
        response = self.client.get(REDACTORS_LIST)
        self.assertNotEqual(response.status_code, 200)

    def test_car_list(self):
        response = self.client.get(NEWSPAPERS_LIST)
        self.assertNotEqual(response.status_code, 200)

    def test_manufacturer_list(self):
        response = self.client.get(TOPICS_LIST)
        self.assertNotEqual(response.status_code, 200)


class TestsForPrivateRequired(TestCase):

    def setUp(self) -> None:
        self.driver = get_user_model().objects.create_user(
            username="test.user",
            password="test123"
        )
        self.client.force_login(self.driver)

    def test_login(self) -> None:
        response = self.client.get(HOME_PAGE)
        self.assertEqual(response.status_code, 200)

    def test_driver_list(self):
        response = self.client.get(REDACTORS_LIST)
        self.assertEqual(response.status_code, 200)

    def test_car_list(self):
        response = self.client.get(NEWSPAPERS_LIST)
        self.assertEqual(response.status_code, 200)

    def test_manufacturer_list(self):
        response = self.client.get(TOPICS_LIST)
        self.assertEqual(response.status_code, 200)
