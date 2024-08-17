from django.urls import include, path
from django.contrib import admin
from .views import welcome


app_name = 'api'

urlpatterns = [
    path('api/v1/', include('api.v1.urls')),
    path('admin/', admin.site.urls),
    path('', welcome, name="welcome"),
]
