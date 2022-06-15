from django.contrib import admin

# Регистрация модели "Задача" для суперюзера (админа)
from .models import Task

# Register your models here.
admin.site.register(Task)
