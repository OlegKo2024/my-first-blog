from django.shortcuts import render, get_object_or_404

# Create your views here.

def post_list_00(request):
    context = {
        'title': 'Главная страница блога'                   # Передаем переменную title в базовый шаблон post_list.html
    }
    return render(request, 'app_blog/post_list.html', context)
    # Используем / слэш когда указываете путь к шаблону в файловой системе  (в этом случае для render), а не когда вызываем
    # Django использует путь в файловой системе относительно директорий шаблонов (TEMPLATES['DIRS'] или app/templates/)
    # Шаблоны ищутся в папке templates внутри приложения. Простое правило:
        # Точка (.) — когда дело связано с Python-кодом (импорты, запуск, модули, классы).
        # Слэш (/) — когда дело связано с файлами и папками (шаблоны, статика, медиа, настройки путей в ОС).

from django.utils import timezone
from .models import Post

def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    context = {
        'title': 'Blog list (BL)',
        'post': posts
    }
    return render(request, 'app_blog/post_list.html', context)

# Объяснение Post.object
# Post — просто описание (какие поля есть у поста)
# Post.objects — "робот-помощник", который умеет работать с базой данных
# Методы — команды этому "роботу"
# Результат — список постов, которые "робот" нашел в базе данных


# Это типичная view-функция в Django, которая обрабатывает HTTP-запрос и возвращает HTTP-ответ
# def post_list(request):
    # post_list — название функции (может быть любым, но обычно соответствует логике, например, home, article_list и т. д.).
    # request — обязательный первый аргумент. Это объект HttpRequest, который содержит:
        # Данные запроса (GET, POST, headers, user, session и т. д.).
        # Методы (request.method, request.GET.get() и др.)
# return render(request, 'app_blog/post_list.html', {})
# Функция возвращает результат работы render(), который формирует HTTP-ответ.
# 📌 render() — это вспомогательная функция Django для рендеринга HTML-шаблона (сборки (putting together) и возврата HttpResponse.
#   Основная цель render() — принять запрос, шаблон и словарь контекстных данных (context) и вернуть HTTP-ответ с отрисованным HTML-контентом
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
        'subtitle': 'About This Blog',
    }
    return render(request, 'app_blog/about.html', my_context)

def home_view(request, *args, **kwargs):
   return render(request, 'app_blog/home.html', {})


def blog_detail_view(request):
    context = {
        'subtitle': 'We Chat Blog Instructions',
    }
    return render(request, 'app_blog/blog.html', context)

def html_rules(request):
    from datetime import date
    posts = Post.objects.filter(
        published_date__date__gte=date(2025, 9, 5)
    ).order_by('published_date')
    context = {
        'title': 'BOOKMARK',
        'posts': posts
    }
    return render(request, 'app_blog/html_rules.html', context)

def new(request):
    posts_items = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date') # ← Переменная Python (QuerySet)
    context = {
        'subtitle': 'Posts List',
        'posts': posts_items    # ← КЛЮЧ 'posts' : ЗНАЧЕНИЕ posts_items, который идет в new.html как связь в {% for item in posts %} - иначе не работает
    }
    return render(request, 'app_blog/new.html', context) # вместо переменной context можно в returns дать {'posts': posts_items})

def post_detail(request, pk):
    post_item = get_object_or_404(Post, pk=pk)
    return render(request, 'app_blog/post_detail.html', {'post': post_item})

"""
Функция post_detail ожидает получить на вход тот самый параметр pk, который был извлечен из URL (<int:pk>). 
Без этого параметра она не сможет найти нужную запись в базе данных
"""

from django.shortcuts import redirect  # ← добавить redirect
from .forms import PostForm

def post_add(request):
    if request.method == "POST":
        # Вот здесь данные из request.POST будут использованы!
        form = PostForm(request.POST)  # ← Ключевое изменение!
            # Почему не PostForm(request)?
                # Объект request содержит МНОГО разной информации: Метод запроса, Cookies, Сессии, Пользователя
                # и Данные формы (request.POST, request.FILES)
                # Форма должна работать только с данными формы, а не со всем запросом.
        if form.is_valid():
            post = form.save(commit=False)  # Не сохранять сразу в БД - (commit=False) - двухшаговое сохранение:
            # Создает объект в памяти, но НЕ сохраняет в базу, позволяет добавить дополнительные данные
            # Требует явного вызова post.save() потом
            post.author = request.user
            post.published_date = timezone.now()
            post.save()                     # Теперь сохраняем в БД
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()   # Создание экземпляра формы
    return render(request, 'app_blog/post_add.html', {'form': form})
    # 'form' - это произвольное имя переменной, которое вы выбираете сами

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)   # added post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)    # added instance=post
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'app_blog/post_edit.html', {'form': form})   # changed for 'app_blog/post_edit.html'

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()  # ← Вот и всё удаление!
        return redirect('new')  # Перенаправляем на список постов
    return render(request, 'app_blog/post_delete.html', {'post': post})


"""
Итог процесса def post_add(request)::
{'form': form} → создает словарь контекста
render() → преобразует в объект Context Django
Шаблон получает доступ к объекту формы через переменную form
{{ form.as_p }} → вызывает методы объекта формы для генерации HTML
Это и есть магия работы шаблонов Django - они "видят" Python объекты, переданные через контекст!

Что происходит в деталях:
1. Создание формы:
    PostForm() вызывает конструктор класса формы Django (см. импорт from .forms import PostForm)
    Создается не связанная (unbound) форма - то есть без привязанных к ней данных
        Не связанная форма = чистый бланк анкеты (без заполненных данных)
        Связанная форма = заполненная анкета с данными пользователя
    Django создает объекты полей на основе определения формы
Подготовка контекста:
    Создается словарь контекста {'form': form}  
    Объект формы добавляется в контекст шаблона
2. Функция render() выполняет:
def render(request, template_name, context=None, content_type=None, status=None):
    # 1. Загрузка шаблона
    template = loader.get_template(template_name)
    # 2. Преобразование context в объект Context
    if context is None:
        context = {}
    # Создается объект Context Django
    context = Context(context, request=request)
    # 3. Рендеринг шаблона с контекстом
    content = template.render(context)
    return HttpResponse(content, content_type=content_type, status=status)
    Шаг 3: Визуализация процесса
До вызова render():
Memory:
┌─────────────────┐
│   form = PostForm()  │ → Объект формы в памяти Python
└─────────────────┘
После создания контекста:
Context object:
┌─────────────────────────────────┐
│ Ключ    │ Значение              │
├─────────────────────────────────┤
│ 'form'  │ <PostForm object>     │ ← Теперь доступен в шаблоне
│ 'request'│ <WSGIRequest object> │
└─────────────────────────────────┘
3. Шаг 3: Обработка наследования шаблонов
{% extends 'app_blog/base_new.html' %}
Загрузка родительского шаблона:
    Django находит и загружает base_new.html
    Определяет блоки, доступные для переопределения
    Построение дерева наследования:
        base_new.html (родитель)
        │
        └── post_add.html (дочерний)
4. Обработка блока content
{% block content %} ... {% endblock %} - Django заменяет блок в родительском шаблоне содержимым из дочернего шаблона.
5. Генерация формы - ключевой этап
Часть 1: CSRF Token - {% csrf_token %} Что генерируется:
    <input type="hidden" name="csrfmiddlewaretoken" value="a1b2c3d4e5f6...">
    Как это работает:
        Django генерирует уникальный токен для каждой сессии
        При POST-запросе middleware проверяет этот токен и защищает от межсайтовой подделки запросов
Часть 2: Рендеринг полей формы - {{ form.as_p }}. Что происходит внутри:
    Итерация по полям формы:
    Django проходит через form.fields в порядке, определенном в классе формы
    Для каждого поля создается HTML-разметка
7. Финальная сборка HTML
8. Отправка формы
Хотя это выходит за рамки рендеринга, полезно понимать полный цикл:
    Пользователь заполняет и отправляет форму
    Django проверяет CSRF токен
    Создается связанная форма с данными: form = PostForm(request.POST)
    Валидация данных и сохранение или возврат ошибок

Демонстрация:
# views.py
def post_new(request):
    form = PostForm()
    return render(request, 'app_blog/post_add.html', {'form': form})
html
<!-- template.html -->
{{ form.as_p }}  <!-- Обращение к переменной 'form' из контекста -->

Django не навязывает имена переменных. Вы сами выбираете:
    Как назвать переменную в Python коде, например, banana > banana = PostForm()
    Какой ключ использовать в словаре контекста, например, worksheet > {'worksheet': banana}
    Главное - чтобы имя в контексте совпадало с именем в шаблоне: {'worksheet': banana} > {{ worksheet.as_p }}
"""

