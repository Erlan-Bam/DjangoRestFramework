from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/token/', DecoratedTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/v1/blogs/users/', UserList.as_view(), name='see-users'),
    path('api/v1/blogs/add-user/', UserAdd.as_view(), name='add-user'),
    path('api/v1/blog/login-user/', LoginUserView.as_view(), name='login_user'),
    path('api/v1/blogs/get-user/<int:id>', UserView.as_view(), name='get-user'),
    path('api/v1/blogs/update-user/<int:user_id>/', UserUpdate.as_view(), name='update-user'),
    path('api/v1/blogs/delete-user/<int:user_id>/', UserDelete.as_view(), name='delete-user'),
    
    path('api/v1/blogs/add-comment/', CommentAdd.as_view(), name='add-comment'),
    path('api/v1/blogs/comments-list/<int:blog_id>/', CommentList.as_view(), name='see-comments'),
    path('api/v1/blogs/<int:blog_id>/delete-comment/<int:comment_id>/', CommentDelete.as_view(), name='delete-comment'),
    path('api/v1/blogs/<int:blog_id>/update-comment/<int:comment_id>/', CommentUpdate.as_view(), name='update-comment'),

    path('api/v1/blogs/add-blog/', BlogAdd.as_view(), name='add-blog'),
    path('api/v1/blogs/blogs-list/', BlogList.as_view(), name='see-blogs'),
    path('api/v1/blogs/delete-blog/<int:blog_id>/', BlogDelete.as_view(), name='delete-blog'),
    path('api/v1/blogs/update-blog/<int:blog_id>/', BlogUpdate.as_view(), name='update-blog'),
]