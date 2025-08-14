from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.conf import settings
import datetime
import jwt

from .models import User
from .serializers import UserSerializer, LoginSerializer, UpdateUserSerializer


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def signup(request):
	"""Register a new user."""
	serializer = UserSerializer(data=request.data)
	if serializer.is_valid():
		user = serializer.save()
		data = UserSerializer(user).data
		return Response(data, status=status.HTTP_201_CREATED)
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def login_view(request):
	"""Login with email and password."""
	serializer = LoginSerializer(data=request.data)
	if not serializer.is_valid():
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	email = serializer.validated_data['email']
	password = serializer.validated_data['password']

	try:
		user = User.objects.get(email=email)
	except User.DoesNotExist:
		return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

	if not check_password(password, user.password):
		return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

	# Create JWT token
	exp_hours = getattr(settings, 'JWT_EXP_HOURS', 24)
	payload = {
		'user_id': user.id,
		'email': user.email,
		'iat': datetime.datetime.utcnow(),
		'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=exp_hours),
	}
	token = jwt.encode(payload, settings.SECRET_KEY, algorithm=getattr(settings, 'JWT_ALGORITHM', 'HS256'))
	if isinstance(token, bytes):
		token = token.decode('utf-8')

	data = {
		'id': user.id,
		'name': user.name,
		'last_name': user.last_name,
		'email': user.email,
		'phone_number': user.phone_number,
		'is_admin': user.is_admin,
		'token': token,
	}
	return Response(data, status=status.HTTP_200_OK)


@api_view(['PUT', 'PATCH'])
def update_me(request):
	"""Update current user's name, last_name, and phone_number."""
	user = request.user
	if not isinstance(user, User):
		return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)

	partial = request.method == 'PATCH'
	serializer = UpdateUserSerializer(instance=user, data=request.data, partial=partial)
	if serializer.is_valid():
		serializer.save()
		return Response({
			'id': user.id,
			'name': user.name,
			'last_name': user.last_name,
			'email': user.email,
			'phone_number': user.phone_number,
		})
	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_me(request):
    """Get current authenticated user's info."""
    user = request.user
    if not hasattr(user, 'id'):
        return Response({'detail': 'Authentication required'}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def check_name_exists(request):
    name = request.query_params.get('name')
    if not name:
        return Response({'detail': 'Name parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
    exists = User.objects.filter(name=name).exists()
    return Response({'exists': exists}, status=status.HTTP_200_OK)

def _require_admin(request):
    user = request.user
    if not hasattr(user, 'is_admin') or not user.is_admin:
        return Response({'detail': 'Admin access required'}, status=status.HTTP_403_FORBIDDEN)
    return None

@api_view(['GET'])
def admin_list_users(request):
    admin_check = _require_admin(request)
    if admin_check:
        return admin_check
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def admin_delete_user(request, pk):
    admin_check = _require_admin(request)
    if admin_check:
        return admin_check
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    user.delete()
    return Response({'detail': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)




