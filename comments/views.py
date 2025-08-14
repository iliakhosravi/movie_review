from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['POST'])
def create_comment(request):
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def list_comments_by_movie(request, movie_id):
    comments = Comment.objects.filter(movie_id=movie_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


def _require_admin(request):
    user = request.user
    if not hasattr(user, 'is_admin') or not user.is_admin:
        return Response({'detail': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    return None


@api_view(['DELETE'])
def admin_delete_comment(request, pk):
    admin_check = _require_admin(request)
    if admin_check:
        return admin_check
    try:
        comment = Comment.objects.get(pk=pk)
    except Comment.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
    comment.delete()
    return Response({'detail': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_my_comments(request):
    comments = Comment.objects.filter(userId=request.user)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
