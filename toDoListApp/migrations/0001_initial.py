# Generated by Django 4.0.4 on 2022-06-14 15:48

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('task_id', models.AutoField(primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('task_name', models.CharField(max_length=50, verbose_name='Название')),
                ('task_description', models.TextField(verbose_name='Описание')),
                ('task_status', models.BooleanField(verbose_name='Статус выполнения')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
            },
        ),
    ]