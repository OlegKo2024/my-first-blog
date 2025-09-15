from django.urls import path
from . import views     # относительный импорт означает "текущий пакет app_blog", import views
                        # абсолютный импорт был бы from app_blog import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('new/', views.new, name='new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail')
]