from django.db import models
from users.models import CustomUser


class Course(models.Model):
    """Модель продукта - курса."""
    title = models.CharField(max_length=250, verbose_name='Название', null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, verbose_name='Автор', null=True, blank=True)
    price = models.DecimalField(max_digits=250, decimal_places=2, verbose_name='Цена', null=True, blank=True)
    start_date = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Дата и время начала курса')

    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    DisplayFields = ["id", "title", "price", "start_date", "created", "updated"]
    SearchableFields = DisplayFields
    FilterFields = ["created", "updated"]

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='Курс', null=True, blank=True)
    title = models.CharField(max_length=250, verbose_name='Название', null=True)
    link = models.URLField(max_length=250, verbose_name='Ссылка', null=True)

    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    DisplayFields = ["id", "title", "course", "link", "created", "updated"]
    SearchableFields = DisplayFields
    FilterFields = ["created", "updated"]

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class UserCourse(models.Model):
    """Доступ к курсам."""
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        verbose_name='Пользователь', related_name='user_courses'
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс', related_name='user_courses')
    enrolled_at = models.DateTimeField(verbose_name='Зарегистрирован:', auto_now_add=True)
    is_active = models.BooleanField(verbose_name='Активный ?', default=True)

    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    DisplayFields = ["id", "user", "course", "enrolled_at", "is_active", "created", "updated"]
    SearchableFields = DisplayFields
    FilterFields = ["created", "updated"]

    class Meta:
        verbose_name = 'Доступ пользователя к курсу'
        verbose_name_plural = 'Доступы пользователей к курсам'
        unique_together = ('user', 'course')
        ordering = ('-id',)

    def __str__(self):
        return self.course.title


class Group(models.Model):
    """Модель группы."""
    title = models.CharField(max_length=250, verbose_name='Название', null=True)
    course = models.ManyToManyField(Course, related_name='courses', verbose_name='Курсы')
    participants = models.ManyToManyField(CustomUser, related_name='participants', verbose_name='Участники')

    @property
    def course_list(self):
        return ", ".join([course.title for course in self.course.all()])

    @property
    def participants_count(self):
        return self.participants.count()

    created = models.DateTimeField(verbose_name='Создано', auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Обновлено', auto_now=True)

    DisplayFields = ["id", "title", "course_list", "participants_count", "created", "updated"]
    SearchableFields = DisplayFields
    FilterFields = ["created", "updated"]

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)

    def __str__(self):
        return self.title
