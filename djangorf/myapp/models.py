from django.db import models

from django.utils.text import slugify

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from datetime import datetime, timedelta

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Please provide an email address')
        if not password:
            raise ValueError('Please provide a password')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    GENDER = {
        'M': 'male',
        'F': 'female',
        'O': 'other',
    }

    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True)
    photo = models.ImageField(upload_to='photos/User/%Y/%m/%d/', blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
    

class Comment(models.Model):
    author = models.ForeignKey('User', on_delete=models.CASCADE, related_name='comments')
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='comments')
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField(max_length=1000)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.author.name} created comment on {self.blog.title}"

class Blog(models.Model):
    publisher = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name='blogs')
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=1000)
    photo = models.ImageField(upload_to='photo/Blog/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    is_published = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.publisher.name} created blog about:{self.title}"


    
