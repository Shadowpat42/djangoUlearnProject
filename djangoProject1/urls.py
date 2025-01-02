from django.contrib import admin
from django.urls import path, include
from main import views  # Импортируем views, если хотим использовать отдельное представление

urlpatterns = [
    path('admin/', admin.site.urls),  # Админка
    path('index/', include('main.urls')),  # Путь для приложения main
    path('', views.index, name='home'),  # Главная страница
    path("statistics/", views.statistics, name="statistics"),
]
