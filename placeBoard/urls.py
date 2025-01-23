from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.board_list),
    path('write/', views.board_write),
    path('detail/<int:pk>/', views.board_detail),
    path('update/<int:pk>/', views.board_update),
    path('upload_image_url/', views.upload_image_view, name='upload_image'),
]