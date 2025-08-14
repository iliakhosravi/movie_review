from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Favorite
from movie.serializers import MovieSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_my_favorites(request):
    favorites = Favorite.objects.filter(userId=request.user)
    movies = [fav.movieId for fav in favorites]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
