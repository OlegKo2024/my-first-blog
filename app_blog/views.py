from django.shortcuts import render

# Create your views here.

def post_list(request):
    context = {
        'title': 'Главная страница блога'                       # Передаем переменную title в базовый шаблон post_list.html
    }
    return render(request, 'app_blog/post_list.html', context)
    # Используем / слэш когда указываете путь к шаблону в файловой системе  (в этом случае для render), а не когда вызываем
    # Django использует путь в файловой системе относительно директорий шаблонов (TEMPLATES['DIRS'] или app/templates/)
    # Шаблоны ищутся в папке templates внутри приложения. Простое правило:
        # Точка (.) — когда дело связано с Python-кодом (импорты, запуск, модули, классы).
        # Слэш (/) — когда дело связано с файлами и папками (шаблоны, статика, медиа, настройки путей в ОС).

# Это типичная view-функция в Django, которая обрабатывает HTTP-запрос и возвращает HTTP-ответ
# def post_list(request):
    # post_list — название функции (может быть любым, но обычно соответствует логике, например, home, article_list и т. д.).
    # request — обязательный первый аргумент. Это объект HttpRequest, который содержит:
        # Данные запроса (GET, POST, headers, user, session и т. д.).
        # Методы (request.method, request.GET.get() и др.)
# return render(request, 'app_blog/post_list.html', {})
# Функция возвращает результат работы render(), который формирует HTTP-ответ.
# 📌 render() — это вспомогательная функция Django для рендеринга HTML-шаблона (приема) и возврата HttpResponse.
#   Основная цель render() — принять запрос, шаблон и словарь контекстных данных и вернуть HTTP-ответ с отрисованным HTML-контентом
# 📌 Аргументы render():
# request
    # Объект запроса (HttpRequest), переданный в view-функцию.
    # 'app_blog/post_list.html' - путь к HTML-шаблону (относительно папки templates).
# Django ищет его в:
    # app_blog/
    # └── templates/
    #     └── app_blog/
    #         └── post_list.html  # <- именно этот файл
    # Почему app_blog/post_list.html, а не просто post_list.html?
        # → Чтобы избежать конфликтов, если в другом приложении есть шаблон с таким же именем.
    # {} (контекст) - Словарь с данными, которые передаются в шаблон.
        # В данном случае он пустой ({}), значит, в шаблон не передаётся никаких переменных.
        # Пример с данными:
            # return render(request, 'app_blog/post_list.html', {
            #     'posts': Post.objects.all(),  # передаём список статей
            #     'title': 'Главная страница'
            # })

# request — обязательный первый аргумент. Это объект HttpRequest, который содержит:
# Данные запроса (GET, POST, headers, user, session и т. д.).
# Методы (request.method, request.GET.get() и др.)

#     Что происходит под капотом?
#       Django получает HTTP-запрос (например, GET /).
#       Вызывается post_list(request).
#       Функция render():
#         Загружает шаблон post_list.html.
#         Рендерит его (подставляет переменные, если они есть).
#         Возвращает HttpResponse с готовым HTML


from django.http import HttpResponse


def contact_view(request, *args, **kwargs):
    return HttpResponse("<h1>Give me some break</h1")


def about_view(request, *args, **kwargs):
    #    return HttpResponse("<h1>Give me some break</h1")
    my_context = {
        'my_text': 'this is about my blog for you',
        'my_number': '+79067073192',
        'my_list': [123, 456, 789, 'abc'],
        'my_html': '<h1>Hello World</h1>'
    }
    return render(request, 'app_blog/about.html', my_context)

def home_view(request, *args, **kwargs):
   return render(request, 'app_blog/home.html', {})