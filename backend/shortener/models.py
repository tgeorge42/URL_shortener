from django.db import models

class ShortenedURL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=6, unique=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
