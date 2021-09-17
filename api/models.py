from django.db import models
from django.utils import timezone
from mdeditor.fields import MDTextField


class Tag(models.Model):
    name = models.CharField(max_length=20)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    tags = models.ManyToManyField(Tag, blank=True)
    title = models.CharField(max_length=200)
    thumbnail = models.ImageField(upload_to='thumbnail/', blank=True, null=True)
    description = models.TextField(blank=True)
    content = MDTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        ordering = ['-published_at']

    def save(self, *args, **kwargs):
        if self.is_public and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ContentImage(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.PROTECT)
    content_image = models.ImageField(upload_to='contents/', blank=True, null=True)
