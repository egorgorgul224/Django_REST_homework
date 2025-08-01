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

Реализована сериализация CourseSerializer для модели Course и LessonSerializer для Lesson.

---

## Приложение User <a id="user_app"></a>

Приложение user создано для создания/редактирования/просмотра и удаления пользователя.

Ниже будут описаны модели, контроллеры + ссылки, сериализации.

### Модели<a id="user_models"></a>

В приложении создана модель:
- User - приложение для ведения пользователей. Содержит поля email, city, phone, avatar.

### Контроллеры и ссылки<a id="user_controllers"></a>

1. Контроллер **UserUpdateAPIView для обновления информации о пользователе. Поля для редактирования: first_name,
last_name, city, phone, avatar.

```
Ссылка для контроллера: адрес/user/id_пользователя/update/
```

### Сериализация<a id="user_serialize"></a>

Реализована сериализация UserSerializer для модели User. Предоставлен доступ к редактированию полей: first_name,
last_name, city, phone, avatar.

---

## Запуск и тестирование проекта<a id="launch"></a>

1. После установки и настройки проекта в консоль введите python/python3 manage.py runserver для запуска сервера.
2. Создание/редактирование/просмотр/удаление моделей проводится в Postman.

---

## Лицензия<a id="license"></a>

Этот проект лицензирован по [лицензии MIT](LICENSE).

##### [Оглавление](#content)