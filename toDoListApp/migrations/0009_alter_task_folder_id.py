# Generated by Django 4.0.4 on 2022-06-16 14:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('toDoListApp', '0008_alter_folder_parent_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='folder_id',
            field=models.ForeignKey(default='Null', null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to='toDoListApp.folder', verbose_name='ID папки'),
        ),
    ]
