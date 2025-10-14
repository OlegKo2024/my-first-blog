from django.urls import path
from . import views     # относительный импорт означает "текущий пакет app_blog", import views
                        # абсолютный импорт был бы from app_blog import views


urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('new/', views.new, name='new'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/add/', views.post_add, name='post_add'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/delete/', views.post_delete, name='post_delete')
]

"""
path('post/<int:pk>/', views.post_detail, name='post_detail')
'post/<int:pk>/' — это шаблон URL (URL pattern).
post/ — статическая часть пути.
<int:pk> — переменная часть пути (converter). Она говорит Django:
"Ожидай здесь целое число (int)";
"И передай его в функцию представления под именем pk (primary key)".
name='post_detail' — это имя маршрута. Вы даете этому конкретному пути уникальное имя, чтобы обращаться к нему в коде по имени, а не по его буквальному адресу.

Шаги:
1. Шаблон → URL (Template → URL): <a href="{% url 'post_detail' pk=item.pk %}">:
    'post_detail' - имя URL-паттерна
    pk=item.pk - передача параметра
    Django генерирует путь: /post/1/ (если item.pk = 1)
2. URL → View (Маршрутизация): path('post/<int:pk>/', views.post_detail, name='post_detail'):
    'post/<int:pk>/' - паттерн пути
    <int:pk> - параметр pk=item.pk
    views.post_detail - вызываем функция 
3. View → Database (Логика): def post_detail(request, pk):
                                post = get_object_or_404(Post, pk=pk)
                                    pk из URL передается в функцию
                                    get_object_or_404 ищет запись или возвращает 404
                                    Находит пост с соответствующим primary key
4. View → Template (Рендеринг): return render(request, 'app_blog/post_detail.html', {'post': post})
    Передает найденный post в шаблон
    Шаблон использует {{ post.title }}, {{ post.text }} и т.д.
Визуализация полного цикла:
text
[Клик по ссылке] 
    ↓
[Генерация URL: /post/1/] 
    ↓  
[URLconf: post/<int:pk>/ → views.post_detail]
    ↓
[View: get_object_or_404(Post, pk=1)] 
    ↓
[База данных: SELECT * FROM post WHERE id = 1]
    ↓  
[Рендеринг шаблона app_blog/post_detail.html' с объектом post]
    ↓
[post_detail.html c с объектом post > HTML страница деталей поста]
"""