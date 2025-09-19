from django.urls import path
from . import views     # относительный импорт означает "текущий пакет app_blog", import views
                        # абсолютный импорт был бы from app_blog import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('new/', views.new, name='new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail')
]

"""
path('post/<int:pk>/', views.post_detail, name='post_detail')
'post/<int:pk>/' — это шаблон URL (URL pattern).
post/ — статическая часть пути.
<int:pk> — переменная часть пути (converter). Она говорит Django:
"Ожидай здесь целое число (int)";
"И передай его в функцию представления под именем pk (primary key)".
name='post_detail' — это имя маршрута. Вы даете этому конкретному пути уникальное имя, чтобы обращаться к нему в коде по имени, а не по его буквальному адресу.
"""