from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Movie
from rest_framework import status
from .serializers import MovieSerializer

def _require_admin(request):
    user = request.user
    if not hasattr(user, 'is_admin') or not user.is_admin:
        return Response({'detail': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    return None

@api_view(['GET'])
def movie_list(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

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


