from rest_framework.exceptions import ValidationError
from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *

from profanity_check  import predict

import re

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.name
        token['email'] = user.email

        return token

class LoginSerializer(TokenObtainPairSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.name
        token['email'] = user.email

        return token
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'description', 'gender', 'photo']
        extra_kwargs = {
            "password": {"write_only": True}
        }
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        Token.objects.create(user=instance)

        return instance
    def validate_name(self, name):
        validate = name.lower()
        if predict([validate]):
            raise ValidationError(detail={"Message": 'Name should not contain bad words!'})
        if re.match(r'^\d', name):
            raise ValidationError(detail={"Message": 'Name should not start with number!'})
        return name
    
    def validate_description(self, description):
        validate = description.lower()
        if predict([validate]):
            raise ValidationError(detail={"Message": 'No bad words in description!'})
        return description

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
    def validate_title(self, title):
        validate = title.lower()
        if predict([validate]):
            raise ValidationError(detail={"Message": 'Title should not contain bad words!'})
        return title
    def validate_content(self, content):
        validate = content.lower()
        if predict([validate]):
            raise ValidationError(detail={"Message": 'Content should not contain bad words!'})
        return content

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data.get('title', ''))
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data['slug'] = slugify(validated_data.get('title', ''))
        return super().update(instance, validated_data)