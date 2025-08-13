from django.db import models
from user.models import User
from movie.models import Movie

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user} on {self.movie}: {self.text[:30]}"
