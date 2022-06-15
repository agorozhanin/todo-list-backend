from django.urls import path

from . import views

# Создание путей
urlpatterns = [
    path('api/task/', views.TaskView.as_view()),
    path('api/task/<int:task_id>/', views.TaskViewForIndexInEnd.as_view())
]
