from django.db import models
from user.models import User
from movie.models import Movie

class Favorite(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    movieId = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.userId.id} likes {self.movieId.id}"
