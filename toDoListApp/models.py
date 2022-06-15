from django.db import models


# Модель задачи
class Task(models.Model):
    # Внутренний класс для корректного отображения множественного числа на русском
    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    # Автоинкрементное поле - ID задачи
    task_id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    # Символьное поле - Название задачи (ограничил 50-ю символами)
    task_name = models.CharField(verbose_name="Название", max_length=50)
    # Текстовое поле - Описание задачи, может быть пустое
    task_description = models.TextField(verbose_name="Описание", null=True)
    # Булевое поле - Статус выполнения, по дефолту False (не выполнено)
    task_status = models.BooleanField(verbose_name="Статус выполнения", default=False)

    # Метод для отображения и идентификации конкретной задачи для пользователя
    def __str__(self):
        return f"Задача {self.task_id}: {self.task_name}"
