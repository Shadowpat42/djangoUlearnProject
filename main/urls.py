from django.urls import path
from . import views  # Импортируем представления из views.py

urlpatterns = [
    path('', views.index, name='index'),  # Путь по умолчанию для /index
]
