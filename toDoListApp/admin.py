from django.contrib import admin

from .models import Task, Folder

# Регистрация модели "Задача" для суперюзера (админа)
admin.site.register(Task)
# Регистрация модели "Папка" для суперюзера (админа)
admin.site.register(Folder)
