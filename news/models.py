from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Redactor(AbstractUser):
    years_of_experience = models.IntegerField(null=True,)

    class Meta:
        verbose_name = "redactor"
        verbose_name_plural = "redactors"
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("news:redactor-detail", kwargs={"pk": self.pk})


class Topic(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Newspaper(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    publishers = models.ManyToManyField(Redactor, related_name="newspapers")

    def __str__(self):
        return f"{self.title}, {self.published_date}"

    class Meta:
        ordering = ['published_date']
