from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Favorite
from movie.models import Movie
from movie.serializers import MovieSerializer



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_my_favorites(request):
    favorites = Favorite.objects.filter(userId=request.user)
    movies = [fav.movieId for fav in favorites]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_favorite(request, pk):
    try:
        favorite = Favorite.objects.get(pk=pk, userId=request.user)
    except Favorite.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    favorite.delete()
    return Response({'detail': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_favorite(request):
    movie_id = request.data.get('movieId')
    if not movie_id:
        return Response({'detail': 'movieId is required'}, status=status.HTTP_400_BAD_REQUEST)
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        return Response({'detail': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    # Prevent duplicate favorites
    if Favorite.objects.filter(userId=request.user, movieId=movie).exists():
        return Response({'detail': 'Already favorited'}, status=status.HTTP_400_BAD_REQUEST)
    favorite = Favorite.objects.create(userId=request.user, movieId=movie)
    return Response({'id': favorite.id, 'movieId': movie.id}, status=status.HTTP_201_CREATED)


