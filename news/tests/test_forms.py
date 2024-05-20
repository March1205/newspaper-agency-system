from django.test import TestCase
from news.forms import (NewspaperSearchForm,
                        TopicSearchForm,
                        RedactorSearchForm,
                        RedactorCreationForm,
                        NewspaperForm)
from news.models import Topic, Redactor


class NewspaperFormTests(TestCase):

    def test_with_valid_data(self) -> None:
        topic = Topic.objects.create(name="Test Topic")
        redactor = Redactor.objects.create_user(
            username="redactor1", password="pass"
        )
        form_data = {
            "title": "Test Newspaper",
            "content": "This is a test newspaper content.",
            "published_date": "2024-05-18",
            "topic": topic.pk,
            "publishers": [redactor.pk]
        }
        form = NewspaperForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self) -> None:
        form_data = {
            "title": "",
            "content": "",
            "published_date": "",
            "topic": None,
            "publishers": []
        }
        form = NewspaperForm(data=form_data)
        self.assertFalse(form.is_valid())


class RedactorCreationFormTests(TestCase):

    def test_with_valid_data(self) -> None:
        form_data = {
            "username": "new_redactor",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
            "years_of_experience": 5,
            "first_name": "John",
            "last_name": "Doe"
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_with_invalid_years_of_experience(self) -> None:
        form_data = {
            "username": "new_redactor",
            "password1": "complexpassword123",
            "password2": "complexpassword123",
            "years_of_experience": -3,
            "first_name": "John",
            "last_name": "Doe"
        }
        form = RedactorCreationForm(data=form_data)
        self.assertFalse(form.is_valid())


class NewspaperSearchFormTests(TestCase):

    def test_with_valid_data(self) -> None:
        form = NewspaperSearchForm(data={"title": "Test News"})
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self) -> None:
        form = NewspaperSearchForm()
        self.assertFalse(form.is_valid())


class RedactorSearchFormTests(TestCase):

    def test_with_valid_data(self) -> None:
        form = RedactorSearchForm(data={"username": "TestUser"})
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self) -> None:
        form = RedactorSearchForm()
        self.assertFalse(form.is_valid())


class TopicSearchFormTests(TestCase):

    def test_with_valid_data(self) -> None:
        form = TopicSearchForm(data={"name": "TestTopic"})
        self.assertTrue(form.is_valid())

    def test_with_invalid_data(self):
        form = TopicSearchForm()
        self.assertFalse(form.is_valid())
