from django.db import models

# Модель папки
from django.db.models.signals import post_init


class Folder(models.Model):
    # Внутренний класс для корректного отображения множественного числа на русском
    class Meta:
        verbose_name = "Папка"
        verbose_name_plural = "Папки"

    # Автоинкрементное поле - ID папки
    folder_id = models.AutoField(verbose_name="ID", primary_key=True, unique=True)
    # Символьное поле - Название папки (ограничил 50-ю символами)
    folder_name = models.CharField(verbose_name="Название папки", max_length=50)
    # Внутренний FK - ID родительской папка
    # Если совпадает с ID этой папки, то родительской нет
    # При удалении папки-родителя, дочерняя папка тоже удаляется
    parent_folder = models.ForeignKey(to='self', verbose_name='ID родительской папки', on_delete=models.CASCADE,
                                      null=True, blank=True)

    # Сигнал (триггер). Если приходит null в FK родительской папки - заменяет его на ID папки
    @staticmethod
    def remember_state(sender, instance, **kwargs):
        if not instance.parent_folder:
            instance.parent_folder = instance

    # Метод для отображения и идентификации конкретной задачи для пользователя
    def __str__(self):
        return f"Папка {self.folder_id}: {self.folder_name}"


post_init.connect(Folder.remember_state, sender=Folder)


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
    # FK ID папки, в которой лежит задача
    # При удалении папки, в которой лежит задача, задача удаляется тоже
    # Задача не обязательно лежит в какой-то папке
    folder_id = models.ForeignKey(to='Folder', verbose_name='ID папки', on_delete=models.CASCADE, null=True,
                                  default=None, blank=True)

    # Метод для отображения и идентификации конкретной задачи для пользователя
    def __str__(self):
        return f"Задача {self.task_id}: {self.task_name}"
