from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True, min_length=6)

	class Meta:
		model = User
		fields = [
			'id',
			'name',
			'last_name',
			'phone_number',
			'email',
			'is_admin',
			'password',
			'bio',
			'favoriteGenre',
			'avatarUrl'
		]

	def create(self, validated_data):
		# Hash the password before saving
		raw_password = validated_data.pop('password')
		validated_data['password'] = make_password(raw_password)
		return super().create(validated_data)


class LoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(write_only=True)


class UpdateUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['name', 'last_name', 'phone_number', 'favoriteGenre', 'bio', 'avatarUrl', 'password']


