from django.urls import path

from . import tasksViews, foldersViews

# Создание путей
urlpatterns = [
    # Для задач
    path('api/task/', tasksViews.TaskView.as_view()),
    path('api/task/<int:task_id>/', tasksViews.TaskViewForIndexInEnd.as_view()),

    # Для папок
    path('api/folder/', foldersViews.FolderView.as_view()),
    path('api/folder/<int:folder_id>/', foldersViews.FolderViewForIndexInEnd.as_view()),
]
