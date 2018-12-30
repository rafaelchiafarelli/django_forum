from django.urls import path
from .forms import PostDetailView
from .views import (
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    home,
    PostList,
    PostDetail,
    )
from . import views

urlpatterns = [
    path('', home, name='blog-home'),
    path('home/', home, name='blog-home'),
    path('user/<str:username>', PostList, name='user-posts'),
    path('user/<int:choice>', PostList, name='choice-posts'),
    path('post/<int:pk>/', PostDetail, name='post-detail'),
    path('post/new/', PostCreateView, name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('post_list/<str:choice>',PostList,name='post-list'),

]
