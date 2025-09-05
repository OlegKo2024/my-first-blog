"""
URL configuration for blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include

# idea here: we define pattens and if entered in browser and found below, then it goes to the specified view
#     path('', include('app_blog.urls') - if '' look for a view in app_blog.urls'

from app_blog.views import contact_view, about_view, home_view, blog_detail_view, html_rules    # абсолютный импорт from app_blog import views
                                                                                        # Как работает:
                                                                                        # Python ищет модуль app_blog в путях из sys.path
                                                                                        # Директория myblog/ есть в sys.path+
                                                                                        # В myblog/ есть папка my_app/ (с __init__.py)
                                                                                        # Python успешно находит и импортирует модуль
                                                                                    # или относительный импорт from ..app_blog import views
                                                                                        # Как работает:
                                                                                        # .. - поднимаемся из blog/ в родительский пакет myblog/
                                                                                        # myblog/ спускаемся в соседний пакет app_blog/
                                                                                        # импортируем модуль views.py
from app_product.views import product_detail_view

urlpatterns = [
    path('admin/', admin.site.urls),        # берем из from django.contrib import admin
    path('', include('app_blog.urls')),     # берем из app_blog.urls
    path('contact/', contact_view),         # берем из views
    path('about/', about_view),
    path('blog/', blog_detail_view),
    path('home/', home_view),
    path('product/', product_detail_view),
    path('html_rules/', html_rules),
]

"""
This line means that for every URL that starts with admin/, Django will find a corresponding view. 
In this case, we're including a lot of admin URLs so it isn't all packed into this small file – it's more readable.

The urlpatterns list in Django is a fundamental component that defines URL routing — it maps specific URL paths to 
corresponding views or other URL configurations. Let’s break down its components in the example:

urlpatterns
    What it is: A Python list that Django scans to match incoming HTTP request URLs against predefined patterns     

path() Function
    Source: Imported from django.urls (e.g., from django.urls import path). 
    What it does: Defines a URL pattern with:
        A string pattern ('admin/'): The URL path to match (relative to the root URL).
        A target (admin.site.urls): What Django should execute/forward to when the URL is matched.
        path(route, view, kwargs=None, name=None)
        
'admin/'
    Route: A string pattern that matches URLs starting with admin/ (e.g., http://yoursite.com/admin/)
admin.site.urls
    Source: Imported from django.contrib.admin (e.g., from django.contrib import admin)
    What it is: A predefined URL configuration for Django’s admin interface
    Includes paths like admin/login/, and routes for model CRUD operations
    How it works: When visiting /admin/, Django delegates further URL 
    handling to the admin site’s built-in URLs:
        В Django "admin site’s built-in URLs" — это не физический файл в вашем проекте, а динамически генерируемая 
        коллекция URL-шаблонов, которые создаются автоматически классом AdminSite из модуля django.contrib.admin.

C добавлением path('', include('app_blog.urls'))
    Django will now redirect everything that comes into 'http://127.0.0.1:8000/' to app_blog.urls 
    and looks for further instructions there.
    Пользователь запрашивает URL, например:
        http://yoursite.com/admin/      → Обрабатывается admin.site.urls
        http://yoursite.com/            → Обрабатывается app_blog.urls
        http://yoursite.com/about/      → Ищется в app_blog.urls
        
    Поиск совпадения (Matching)
        Django проверяет urlpatterns сверху вниз:
            Проверяет admin/:
            Если URL начинается с admin/, делегирует оставшуюся часть (/ или /login/ и т.д.) admin.site.urls.
                Например, для /admin/login/ Django: 
                Отрезает admin/ → остаётся login/
                Передаёт login/ в admin.site.urls для дальнейшего matching
            Если URL не начинается с admin/, переходит к path('', ...):
                '' (пустая строка) означает корневой путь (/)
                include('blog.urls') говорит Django:
                    Отрезать совпавшую часть (здесь — ничего, так как '').
                    Передать оставшийся путь (весь URL) в blog.urls для дальнейшего matching
        



"""
