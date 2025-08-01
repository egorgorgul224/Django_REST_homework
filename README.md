# Модуль "Django REST Framework"

---

## Оглавление

<a id="content"></a>

1. [Описание](#description)
2. [Установка и настройка проекта](#instruction)
3. [Структура проекта](#structure)
4. [Приложения](#apps)
   - [Приложение materials](#materials_app) 
     - [Модели](#materials_models) 
     - [Контроллеры и ссылки](#materials_controllers)
     - [Сериализация](#materials_serialize)
   - [Приложение Users](#users_app)
     - [Модели](#users_models) 
     - [Контроллеры и ссылки](#users_controllers)
     - [Сериализация](#users_serialize)
     - [Кастомные команды](#users_commands)
6. [Запуск и тестирование проекта](#launch)
7. [Лицензия](#license)

---

## Описание<a id="description"></a>

В проекте изучается и реализуется проект на REST Framework.

---

## Установка и настройка проекта<a id="instruction"></a>

1. Клонируйте репозиторий:

```
git clone https://github.com/username/project-x.git
```

2. Перейдите в директорию проекта:

```
cd ваш_проект
```

3. Установите зависимости проекта:

```
poetry install
```

4. Зайдите в файл .env.example и следуйте инструкциям из него.

---

## Структура проекта<a id="structure"></a>

```
.
├── config
│     ├── asgi.py, settings.py, urls.py, wsgi.py необходимые модули для работы приложения
├── materials - приложение на django
│ ├── migrations - папка с миграциями
│ ├── admin.py, apps.py, models.py, serializers.py, tests.py, urls.py, views.py - модули для работы приложения
├── media
│ ├── avatars - фото для профиля пользователя
│ ├── lesson_video - видео для урока
│ ├── previews - фото для превью курса
├── static - папка со стилями и фото
│ ├── css
│     ├── bootstrap.min.css
│ ├── images
│ ├── js
│     ├── bootstrap.bundle.min.js
├── users - приложение на django
│ ├── management
│     ├── commands - папка с командами
│         ├── add_payments - команда для загрузки платежей в базу данных
│ ├── migrations - папка с миграциями
│ ├── templates - папка с шаблонами страниц
│ ├── admin.py, apps.py, models.py, serializers.py, tests.py, urls.py, views.py - модули для работы приложения
├── .env.example - env экземпляр для доступа к закрытым данным
├── .flake8
├── .gitignore
├── manage.py
├── pyproject.toml
├── poetry.lock
├── requirements.text - файл с зависимостями
└── README.md
```

---

## Приложения<a id="apps"></a>

В проекте реализовано 2 приложения:
1. **materials**: приложение для ведения курсов и уроков в курсах.
2. **users**: приложения для создания/редактирования/просмотра и удаления пользователя.

---

## Приложение Materials <a id="materials_app"></a>

Приложение materials создано для ведения курсов и уроков в курсах.

Ниже будут описаны модели, контроллеры + ссылки, сериализации.

### Модели<a id="materials_models"></a>

В приложении создано 2 модели:
- Course - приложение учебного курса. Содержит поля name, preview(изображение/превью курса), description.
- Lesson - приложение урока. Содержит поля name, description, preview(изображение/превью курса), video_url(ссылка
на видео).

### Контроллеры и ссылки<a id="materials_controllers"></a>

1. Контроллер **CourseViewSet** для создания и удаления курса, вывода списка курсов и информации о каждом курсе.

```
Ссылка для контроллера: адрес/courses/
```

2. Контроллеры модели **Lesson**.
   - Контроллер LessonCreateAPIView для создания урока.
   - Контроллер LessonListAPIView для вывода списка уроков.
   - Контроллер LessonRetrieveAPIView для вывода информации об уроке.
   - Контроллер LessonUpdateAPIView для обновления информации об уроке.
   - Контроллер LessonDestroyAPIView для удаления урока.

```
Ссылка для контроллера LessonListAPIView: адрес/lessons/
Ссылка для контроллера LessonCreateAPIView: адрес/lesson/create/
Ссылка для контроллера LessonRetrieveAPIView: адрес/lesson/<int:pk>/detail/
Ссылка для контроллера LessonDestroyAPIView: адрес/esson/<int:pk>/delete/
Ссылка для контроллера LessonUpdateAPIView: адрес/lesson/<int:pk>/update/
```

### Сериализация<a id="materials_serialize"></a>

Реализована 2 сериализации:
1. CourseSerializer - сериализатор для модели Course. Meta класс передает все поля. Для сериализатора добавлено новое
поле: lesson_count - для отображения количества уроков в курсе. Для поля реализован метод get_lesson_count для
подсчета количества уроков в курсе.

```
def get_lesson_count(self, obj):
    return obj.lessons.count()

'lessons' - related_name поля 'course' модели Lesson.
```

2. LessonSerializer - сериализатор для модели Lesson. Meta класс передает все поля.

---

## Приложение User <a id="users_app"></a>

Приложение User создано для создания/редактирования/просмотра и удаления пользователя, а также для ведения платежей
пользователей по курсам.

Ниже будут описаны модели, контроллеры + ссылки, сериализации.

### Модели<a id="users_models"></a>

В приложении создано 2 модели:
- User - модель пользователь. Содержит поля email, city, phone, avatar.
- Payment - модель платежа. Содержит поля user(модель User), created_at(автозаполнение), course(модель Course),
lesson(модель Lesson), amount, method(способ оплаты: наличные или перевод на счет).

### Контроллеры и ссылки<a id="users_controllers"></a>

1. Контроллер **UserUpdateAPIView для обновления информации о пользователе. Поля для редактирования: first_name,
last_name, city, phone, avatar.

```
Ссылка для контроллера: адрес/user/id_пользователя/update/
```

### Сериализация<a id="users_serialize"></a>

Реализована сериализация UserSerializer для модели User. Предоставлен доступ к редактированию полей: first_name,
last_name, city, phone, avatar.

### Кастомные команды<a id="users_commands"></a>

В приложении реализованы следующие команды:

1. add_payments - - команда для добавления платежей в базу данных. При вызове команды происходит удаление текущих
платежей и загрузка платежей из файла payments_fixture.json.

Команда в консоль: 
```
python manage.py add_payments
```

---

## Запуск и тестирование проекта<a id="launch"></a>

1. После установки и настройки проекта в консоль введите python/python3 manage.py runserver для запуска сервера.
2. Создание/редактирование/просмотр/удаление моделей проводится в Postman.

---

## Лицензия<a id="license"></a>

Этот проект лицензирован по [лицензии MIT](LICENSE).

##### [Оглавление](#content)