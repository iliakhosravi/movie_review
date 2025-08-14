from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=200)
    genre = models.CharField(max_length=100)
    year = models.IntegerField()
    director = models.CharField(max_length=100)
    rating = models.FloatField()
    description = models.TextField()
    poster = models.CharField(max_length=300)  # or use ImageField if you want file upload
    videoUrl = models.CharField(max_length=300)
    releaseDate = models.DateTimeField(null=True, blank=True)
    trailer = models.CharField(max_length=300, null=True, blank=True)
    cast = models.CharField(max_length=500, null=True, blank=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return self.title
