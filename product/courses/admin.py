from django.contrib import admin
from . import models


@admin.register(models.Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = models.Course.DisplayFields
    search_fields = models.Course.SearchableFields
    list_filter = models.Course.FilterFields


@admin.register(models.Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = models.Lesson.DisplayFields
    search_fields = models.Lesson.SearchableFields
    list_filter = models.Lesson.FilterFields


@admin.register(models.Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = models.Group.DisplayFields
    search_fields = models.Group.SearchableFields
    list_filter = models.Group.FilterFields


@admin.register(models.UserCourse)
class UserCourseAdmin(admin.ModelAdmin):
    list_display = models.UserCourse.DisplayFields
    search_fields = models.UserCourse.SearchableFields
    list_filter = models.UserCourse.FilterFields
