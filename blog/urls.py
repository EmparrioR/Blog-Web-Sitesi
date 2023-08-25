from django.urls import path
from . import views
from .views import kategoriye_gore_listele, CategoryListCreateView, CommentListCreateView, PostListCreateView
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView




urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('comment/reply/<int:pk>/', views.reply_to_comment, name='reply_to_comment'),
    path('category_list/', views.category_list, name='category_list'),
    path('kategori/<str:category_name>/', kategoriye_gore_listele, name='kategoriye_gore_listele'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('comment/<int:pk>/delete/', views.comment_delete, name='comment_delete'),
    path('post_list/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('account/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('hesabim/', views.hesabim , name='hesabim'),
    path('register/', views.register, name='register'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('create_category/', views.create_category, name='create_category'),
    path('api/get_subcategories/<str:category_name>/', views.get_subcategories, name='get_subcategories'),
    
    path('categories/', CategoryListCreateView.as_view(authentication_classes=[JWTAuthentication], permission_classes=[IsAuthenticated]), name='category-list-create'),
    path('comments/', CommentListCreateView.as_view(authentication_classes=[JWTAuthentication], permission_classes=[IsAuthenticated]), name='comment-list-create'),
    path('posts/', PostListCreateView.as_view(authentication_classes=[JWTAuthentication], permission_classes=[IsAuthenticated]), name='post-list-create'), 

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # Token alımı
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]   