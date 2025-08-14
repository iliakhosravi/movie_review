from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Movie
from rest_framework import status
from .serializers import MovieSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from comments.models import Comment
from django.db import models


def _require_admin(request):
    user = request.user
    if not hasattr(user, 'is_admin') or not user.is_admin:
        return Response({'detail': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    return None

@api_view(['GET'])
@permission_classes([AllowAny])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def movie_detail(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = MovieSerializer(movie)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def increase_view_count(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    movie.views += 1
    movie.save()
    return Response({'detail': 'View count increased'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def movie_quality(request, pk):
    comments = Comment.objects.filter(movieId=pk)
    if not comments.exists():
        return Response({'average_rating': None, 'quality': 'No ratings'}, status=status.HTTP_200_OK)
    avg = comments.aggregate(models.Avg('rating'))['rating__avg']
    if avg >= 8:
        quality = "Excellent"
    elif avg >= 6:
        quality = "Good"
    elif avg >= 4:
        quality = "Average"
    else:
        quality = "Poor"
    return Response({'average_rating': avg, 'gradeByUsersReview': quality}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def suggest_movies(request):
    favorite_genre = getattr(request.user, 'favoriteGenre', None)
    if not favorite_genre:
        return Response({'detail': 'No favorite genre set for user.'}, status=status.HTTP_400_BAD_REQUEST)
    movies = Movie.objects.filter(genre__icontains=favorite_genre)
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes([AllowAny])
def update_movie_rating(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    
    rating = request.data.get('rating')
    if rating is None:
        return Response({'detail': 'Rating is required'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        rating = float(rating)
        movie.rating = rating
        movie.save()
        return Response({'rating': movie.rating}, status=status.HTTP_200_OK)
    except (ValueError, TypeError):
        return Response({'detail': 'Invalid rating value'}, status=status.HTTP_400_BAD_REQUEST)


# ----------------------- Admin --------------------------


@api_view(['POST'])
def admin_create_movie(request):
    admin_check = _require_admin(request)
    if admin_check:
        return admin_check
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'PATCH'])
def admin_edit_movie(request, pk):
    admin_check = _require_admin(request)
    if admin_check:
        return admin_check
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = MovieSerializer(movie, data=request.data, partial=(request.method == 'PATCH'))
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def admin_delete_movie(request, pk):
    admin_check = _require_admin(request)
    if admin_check:
        return admin_check
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    movie.delete()
    return Response({'detail': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)



