from .serializers import *
from .models import *
from .permissions import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import (
    TokenBlacklistView,
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    
    refresh["user"] = UserSerializer(user).data
    
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class DecoratedTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: MyTokenObtainPairSerializer,
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

#My class views

class LoginUserView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(tags=['Login'], request_body=LoginSerializer)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if(User.objects.filter(email=email).exists()):
            user = User.objects.get(email=email)
            if(user.check_password(password)):
                serializer = UserSerializer(user)
                token = get_tokens_for_user(user)
                return Response({"token": token, "user": serializer.data}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Incorrect password"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "No user with such email"}, status=status.HTTP_404_NOT_FOUND)


    def get(self, request):
        response = {
            "user": str(request.user),
            "auth": str(request.auth)
        }
        return Response(response, status=status.HTTP_200_OK)
class UserView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    @swagger_auto_schema(
        tags=['User'],
    )
    def get(self, request, id):
        user = User.objects.get(pk=id)
        serializer = UserSerializer(user)
        tokens = get_tokens_for_user(user)
        return Response({"user": serializer.data, "token": tokens})

class UserList(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        user = User.objects.all()
        serializer = UserSerializer(user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class UserAdd(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny,)
    @swagger_auto_schema(
        request_body=UserSerializer, tags=['User'],
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if(serializer.is_valid()):
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({'user': serializer.data, 'tokens': tokens}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserUpdate(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = (AllowAny,)
    @swagger_auto_schema(request_body=UserSerializer, tags=['User'])
    def put(self, request, user_id):
        user = User.objects.get(pk=user_id)
        serializer = UserSerializer(user, data=request.data)
        if(serializer.is_valid()):
            user = serializer.save()
            tokens = get_tokens_for_user(user)
            return Response({"user": serializer.data, "token": tokens}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserDelete(APIView):
    @swagger_auto_schema(tags=['User'])
    def delete(self, request, user_id):
        user = User.objects.get(pk=user_id)
        user.delete()
        return Response({"Message": "User successfully deleted"}, status=status.HTTP_200_OK)
    
class CommentDelete(APIView):
    def comment_exists(blog_id, comment_id):
        return Comment.objects.filter(blog_id=blog_id, id=comment_id).exists()
    def delete(self, request, comment_id, blog_id):
        if self.comment_exists(blog_id, comment_id):
            comment = Comment.objects.get(pk=comment_id)
            comment.delete()
            return Response({"Message": "Comment successfully deleted"}, status=status.HTTP_200_OK)
        else:
            return Response({"Message": f"Comment is not found in {blog_id}"}, status=status.HTTP_404_NOT_FOUND)
class CommentUpdate(APIView):
    @swagger_auto_schema(request_body=CommentSerializer,tags=['Comment'])
    def put(self, request, comment_id, blog_id):
        if self.comment_exists(blog_id, comment_id):
            comment = Comment.objects.get(pk=comment_id)
            serializer = CommentSerializer(comment, data=request.data)
            if(serializer.is_valid()):
                serializer.save()
                return Response({"Message": "Updated comment successfully"}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Message": f"Comment is not found in {blog_id}"}, status=status.HTTP_404_NOT_FOUND)
    def comment_exists(blog_id, comment_id):
        return Comment.objects.filter(blog_id=blog_id, id=comment_id).exists()
class CommentList(APIView):
    @swagger_auto_schema(tags=['Comment'])
    def get(self, request, blog_id):
        comments = Blog.objects.get(pk=blog_id).comments
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
class CommentAdd(APIView):
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(request_body=CommentSerializer, tags=['Comment'])
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BlogUpdate(APIView):
    parser_classes = (MultiPartParser, FormParser)
    @swagger_auto_schema(request_body=BlogSerializer, tags=['Blog'])
    def put(self, request, blog_id):
        blog = Blog.objects.get(id=blog_id)
        serializer = BlogSerializer(blog, many=True)
        if(serializer.is_valid()):
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)  
class BlogAdd(APIView):
    parser_classes = (MultiPartParser, FormParser)
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=BlogSerializer, tags=['Blog'])
    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class BlogDelete(APIView):
    @swagger_auto_schema(tags=['Blog'])
    def delete(self, request, blog_id):
        blog = Blog.objects.get(id=blog_id)
        blog.delete()
        return Response({"Message": "Blog succesfully deleted"} ,status=status.HTTP_200_OK)
class BlogList(APIView):
    parser_classes = (MultiPartParser, FormParser)
    
    @swagger_auto_schema(tags=['Blog'])
    def get(self, request):
        blogs = Blog.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)