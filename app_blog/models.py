from django.db import models        # # этот модуль основа для создания моделей базы данных в Django - pre-entered

# Create your models here

from django.conf import settings    # предоставляет доступ к настройкам Django вашего проекта, но есть но
# Это встроенный модуль Django, который отвечает за конфигурацию. Внутри него лежит файл settings.py (не путай с
# settings.py проекта!). После from django.conf import settings:
    # Сначала загружает настройки из global_settings.py (базовые значения Django).
    # Затем перезаписывает их значениями из твоего settings.py (если ты их определил).
    # Даёт доступ к итоговым настройкам через этот объект
from django.utils import timezone   # модуль предоставляет функции для работы с датами и временем с учетом временных зон


class Post(models.Model):   # this line defines our model (it is шаблон (описание структуры), а не конкретный объект)
                            # Post is the name of our model. We can give it a different name (but we must avoid special
                            # characters and whitespace). Always start a class name with an uppercase letter.
                            # models.Model means that the Post is a Django Model, Django knows it to be saved in the db
    # Now we define the properties: title, text, created_date, published_date and author.
    # To do that we need to define the type of each field (text? A number? A date? A relation to another object, like a User?)
    author          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  #  this is a link to another model
    title           = models.CharField(max_length=200)    # this is how you define text with a limited number of characters - have to use max_length=
    text            = models.TextField()                  # this is for long text without a limit. If do not want text then blank=True null=True
    price           = models.DecimalField(default=0.00, max_digits=5, decimal_places=2) # пробую с полем цифр, default=0.00,
                            # ставит 0.00 по уже # введенным данным и будет ставить по новым, если не определить
    featured        = models.BooleanField(default=False)
    created_date    = models.DateTimeField(default=timezone.now)    # this is a date and time
    published_date  = models.DateTimeField(blank=True, null=True)
                            # Значение	    Поведение
                            # blank=True	Поле необязательно для заполнения в формах (админка, ModelForm). Можно оставить пустым.
                            # blank=False	Поле обязательно к заполнению. Если оставить пустым — будет ошибка валидации
                                # blank - обязательность заполнения
                            # Значение	    Поведение
                            # null=True	    В базе данных будет храниться NULL (пустое значение). Разрешено отсутствие значения.
                            # null=False	В базе запрещён NULL. Поле всегда должно иметь значение (например, текущую дату)
                                # null — хранение в базе данных

# Вы абсолютно правы: класс Post(models.Model) определяет таблицу в базе данных. Django ORM (Object-Relational Mapping)
# работает похоже на SQLAlchemy:
    # Класс Post → таблица app_blog_post (Django автоматически создаёт имя таблицы в формате appname_modelname).
    # Атрибуты класса (author, title, text и т. д.) → колонки в таблице.
    # models.CharField → VARCHAR, models.TextField → TEXT, models.DateTimeField → DATETIME и т. д.
# Как работает ForeignKey?
    # Поле author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) делает две ключевые вещи:
    # a) Связь между таблицами
    # В базе данных создаётся колонка author_id, которая хранит id пользователя из таблицы auth_user.
        # таблица auth_user создаётся автоматически, если используете стандартную систему аутентификации Django (django.contrib.auth)
        # Когда вы добавляете django.contrib.auth в INSTALLED_APPS (есть по умолчанию), Django при миграциях создаёт таблицы:
            # auth_user (для хранения пользователей)
            # auth_group, auth_permission и др.
        # Если не меняли AUTH_USER_MODEL в настройках (settings.py), то settings.AUTH_USER_MODEL ссылается именно на auth.User
            # По умолчанию Django использует модель пользователя из django.contrib.auth (это встроенная модель User)
            # В вашем settings.py нет AUTH_USER_MODEL, потому что вы используете стандартную модель auth.User
                # Когда settings.AUTH_USER_MODEL Django ищет модель, делает проверку settings.AUTH_USER_MODEL:
                    # Если settings.py нет AUTH_USER_MODEL → Django берёт значение из django/conf/global_settings.py
                    # AUTH_USER_MODEL = 'auth.User'  # Дефолтное значение
    # При запросе post.author Django автоматически делает SQL-запрос вида:
        # SELECT * FROM auth_user WHERE id = {post.author_id};
    # b) on_delete=models.CASCADE
    # Это правило для базы данных: Если пользователь (auth_user) удаляется, все его посты (Post) тоже удаляются.
    # Альтернативы:
        # PROTECT — запретить удаление, если есть связанные посты
        # SET_NULL — установить author_id = NULL (если поле допускает null=True)
        # SET_DEFAULT — установить значение по умолчанию


    def publish(self):
        self.published_date = timezone.now()    # Устанавливает текущую дату/время
        self.save()                             # Сохраняет объект в БД

# Что делает self.save()?
    # Если запись новая (id=None):
        # Django выполняет INSERT в базу данных:
        # INSERT INTO blog_post (author_id, title, text, created_date, published_date)
        # VALUES (1, 'Заголовок', 'Текст', '2024-01-01 12:00', '2024-01-02 15:30')
    # Если запись уже существует:
        # Django делает UPDATE:
        # UPDATE blog_post
        # SET published_date = '2024-01-02 15:30'
        # WHERE id = 5;
# Где вызывается publish()?
    # Обычно это происходит:
    # В представлениях (views) при публикации поста:
        # def publish_post(request, post_id):
        #     post = Post.objects.get(id=post_id)
        #     post.publish()                                # Вот он!
        #     return HttpResponse("Пост опубликован!")
    # В админке Django (если добавить метод в actions).
    # В командах управления (management commands)

    def __str__(self):
        return f"{self.title} published: {self.published_date} (автор: {self.author})"
# Если в коде сделать:
# post = Post.objects.get(id=1)
# print(post)  # вызовется book.__str__()


# Вывод
# Ваша модель Post — это таблица в БД с колонками author_id, title, text и т. д.
# ForeignKey создаёт связь с таблицей пользователей через author_id.
# publish() меняет published_date и вызывает save(), который делает INSERT или UPDATE в БД.
# Всё это работает благодаря Django ORM, который превращает Python-код в SQL-запросы.
