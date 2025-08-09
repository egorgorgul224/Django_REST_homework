from rest_framework.pagination import PageNumberPagination


class CourseLessonListPaginator(PageNumberPagination):
    """Пагинатор для вывода списка курсов и уроков. Выводит 5 элементов на страницу. Пользователь может увеличить
    количество выводимых объектов до 10."""

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10
