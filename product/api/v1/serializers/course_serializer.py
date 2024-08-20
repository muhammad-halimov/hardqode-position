from django.contrib.auth import get_user_model
from django.db.models import Avg, Count
from rest_framework import serializers
from .user_serializer import CustomUserSerializer
from courses.models import Course, Group, Lesson
from users.models import Subscription

User = get_user_model()


class LessonSerializer(serializers.ModelSerializer):
    """Список уроков."""

    course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class MiniLessonSerializer(serializers.ModelSerializer):
    """Список названий уроков для списка курсов."""

    class Meta:
        model = Lesson
        fields = (
            'title',
        )


class CreateLessonSerializer(serializers.ModelSerializer):
    """Создание уроков."""

    class Meta:
        model = Lesson
        fields = (
            'title',
            'link',
            'course'
        )


class StudentSerializer(serializers.ModelSerializer):
    """Студенты курса."""

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
        )


class MiniCourseSerializer(serializers.ModelSerializer):
    """Список названий курсов."""
    class Meta:
        model = Course
        fields = (
            'title',
            'price'
        )


class GroupSerializer(serializers.ModelSerializer):
    """Список групп."""
    participants_count = serializers.SerializerMethodField(read_only=True)
    participants = CustomUserSerializer(many=True, read_only=True)
    course = MiniCourseSerializer(many=True, read_only=True)
    available_spots = serializers.SerializerMethodField(read_only=True)

    def get_participants_count(self, obj):
        """Количество участников в группе."""
        return obj.participants.count()

    def get_available_spots(self, obj):
        """Количество доступных мест в группе."""
        total_capacity = 10
        return total_capacity - self.get_participants_count(obj)

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
            'participants',
            'participants_count',
            'available_spots',
        )


class CreateGroupSerializer(serializers.ModelSerializer):
    """Создание групп."""

    class Meta:
        model = Group
        fields = (
            'title',
            'course',
        )


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    lessons = MiniLessonSerializer(many=True, read_only=True, source='lesson_set')
    lessons_count = serializers.SerializerMethodField(read_only=True)
    students_count = serializers.SerializerMethodField(read_only=True)
    groups_filled_percent = serializers.SerializerMethodField(read_only=True)
    demand_course_percent = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        """Количество уроков в курсе."""
        return obj.lesson_set.count()

    def get_students_count(self, obj):
        """Общее количество студентов на курсе."""
        return Subscription.objects.filter(course=obj).count()

    def get_groups_filled_percent(self, obj):
        """Процент заполнения групп, если в группе максимум 30 чел.."""
        groups = Group.objects.filter(course=obj)
        total_capacity = groups.count() * 10
        total_students = self.get_students_count(obj)
        if total_capacity == 0:
            return 0
        return (total_students / total_capacity) * 100

    def get_demand_course_percent(self, obj):
        """Процент приобретения курса."""
        total_courses_sold = Subscription.objects.filter(course=obj).count()
        total_courses_available = Course.objects.count()

        if total_courses_available == 0:
            return 0
        return (total_courses_sold / total_courses_available) * 100

    class Meta:
        model = Course
        fields = (
            'id',
            'author',
            'title',
            'start_date',
            'price',
            'lessons_count',
            'lessons',
            'demand_course_percent',
            'students_count',
            'groups_filled_percent',
        )


class CreateCourseSerializer(serializers.ModelSerializer):
    """Создание курсов."""

    class Meta:
        model = Course
        fields = '__all__'
