from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add_directory/', views.add_directory, name='add_directory'),
    path('add_file/', views.add_file, name='add_file'),
    path('view_file/<int:file_id>/', views.view_file, name='view_file'),
]
