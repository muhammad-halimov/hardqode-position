from rest_framework.permissions import BasePermission
from users.models import Subscription


class IsStudentOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        elif request.user.is_authenticated:
            course_id = view.kwargs.get('id')
            if course_id:
                try:
                    subscription = Subscription.objects.get(user=request.user, course=course_id, is_active=True)
                    return True
                except Subscription.DoesNotExist:
                    return False
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        elif request.user.is_authenticated:
            # Check if the user has an active subscription for the object's course
            try:
                subscription = Subscription.objects.get(user=request.user, course=obj.course.id, is_active=True)
                return True
            except Subscription.DoesNotExist:
                return False
        return False


class ReadOnlyOrIsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or request.method in SAFE_METHODS
