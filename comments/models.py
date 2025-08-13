from django.db import models
from user.models import User
from movie.models import Movie

class Comment(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    movieId = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    userName = models.CharField(max_length=100, null=True, blank=True)  # Optional field for user name
    text = models.TextField()
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.movie}: {self.text[:30]}"
