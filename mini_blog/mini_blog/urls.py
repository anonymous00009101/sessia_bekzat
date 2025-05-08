from django.contrib import admin
from django.urls import path, include
from blog import views as blog_views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Mini Blog API",
        default_version='v1',
        description="API documentation for Mini Blog",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@miniblog.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),  # Все API маршруты
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('', blog_views.home, name='home'),  # Подключаем представление home для корневого URL
    path('accounts/', include('django.contrib.auth.urls')),  # Подключение стандартных маршрутов аутентификации
]