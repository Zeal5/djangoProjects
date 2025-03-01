from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model


# Create your models here.
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.TextField(max_length=250)
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="blog_posts"
    )

    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    status = models.CharField(
        choices=Status.choices, default=Status.DRAFT, max_length=2
    )

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    objects = models.Manager()
    published = PublishedManager()
    def __str__(self) -> str:
        return str(self.title)
