from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('posts/<int:id>/', views.post_detail, name='post_detail'),
    path('posts/<int:id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:id>/publish/', views.post_publish, name='post_publish'),
    path('post/add/', views.post_add, name='post_add'),
    path('comment/<int:id>/add/', views.add_comment, name='add_comment'),
]
