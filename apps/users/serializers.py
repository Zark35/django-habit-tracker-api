"""
Users app serializers.
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'bio', 'avatar', 'is_active', 'created_at']
        read_only_fields = ['id', 'is_active', 'created_at']


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm']
    
    def validate(self, data):
        """Validate password confirmation."""
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': 'Passwords do not match.'
            })
        return data
    
    def create(self, validated_data):
        """Create user with validated data."""
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    """Serializer for user login."""
    
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        """Validate login credentials."""
        user = authenticate(
            username=data.get('email'),
            password=data.get('password')
        )
        
        if not user:
            raise serializers.ValidationError(
                'Invalid email or password.'
            )
        
        if not user.is_active:
            raise serializers.ValidationError(
                'This user account is inactive.'
            )
        
        data['user'] = user
        return data


class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile."""
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'bio', 'avatar']


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for user information."""
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'bio', 'avatar', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
