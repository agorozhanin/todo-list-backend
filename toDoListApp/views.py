# Create your views here.

import json

from django.core.serializers import serialize
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Task
from .validators import *


# Класс для передачи данных о задачах с путём без индекса(id) экземпляра сущности в конце
@method_decorator(csrf_exempt, name='dispatch')
class TaskView(View):

    # Метод для получения всех задач
    def get(self, request):

        tasks = Task.objects.all()

        task_serialized_data = serialize('python', tasks)

        count_of_instance = Task.objects.count()

        instance_output_list_of_dicts = list(dict())
        for i in range(count_of_instance):
            task_id = task_serialized_data[i]['pk']
            fields_task_dict = task_serialized_data[i]['fields']
            fields_task_dict['task_id'] = task_id
            instance_output_list_of_dicts.append({'task_id': task_id,
                                                  'task_name': fields_task_dict['task_name'],
                                                  'task_description': fields_task_dict['task_description'],
                                                  'task_status': fields_task_dict['task_status']})

        output_data = {
            "tasks": instance_output_list_of_dicts
        }

        return JsonResponse(output_data, safe=False)

    # Метод для создания задачи
    def post(self, request):

        post_body = json.loads(request.body)

        task_name = post_body.get('task_name')
        task_description = post_body.get('task_description')
        task_status = post_body.get('task_status')

        task_data = {
            'task_name': task_name,
            'task_description': task_description,
            'task_status': task_status,
        }

        if task_name is not None and task_status is not None:

            if is_status(task_status) and is_correct_name(task_name):
                task_object = Task.objects.create(**task_data)
                data = {
                    'task_id': task_object.task_id,
                    'task_name': task_object.task_name,
                    'task_description': task_object.task_description,
                    'task_status': task_object.task_status
                }
                return JsonResponse(data, status=201)

            elif not is_status(task_status) and is_correct_name(task_name):
                data = {
                    'message': 'New task object has not been created because task_status must been boolean type'
                }
                return JsonResponse(data, status=404)

            elif is_status(task_status) and not is_correct_name(task_name):
                data = {
                    'message': 'New task object has not been created because task_name must not been a space or a '
                               'sequence of space'
                }
                return JsonResponse(data, status=404)

            else:
                data = {
                    'message': 'New task object has not been created because task_name must not been a space or a '
                               'sequence of space and task_status must been boolean type'
                }
                return JsonResponse(data, status=404)

        elif task_name is None and task_status is not None:
            if is_status(task_status):
                data = {
                    'message': 'New task object has not been created because task_name is null (is none)'
                }
                return JsonResponse(data, status=404)

            else:
                data = {
                    'message': 'New task object has not been created because task_name is null (is none) and '
                               'task_status must been boolean type'
                }
                return JsonResponse(data, status=404)

        elif task_status is None and task_name is not None:
            if is_correct_name(task_name):
                data = {
                    'message': 'New task object has not been created because task_status is null (is none). It must be '
                               'True or False'
                }
                return JsonResponse(data, status=404)

            else:
                data = {
                    'message': 'New task object has not been created because task_status is null (is none). It must '
                               'be True or False and task_name must not been a space or a sequence of space '
                }
                return JsonResponse(data, status=404)

        else:
            data = {
                'message': 'New task object has not been created because task_name is null (is none) and task_status '
                           'is null (is none). Task_status must been boolean type and task_name must not been a space '
                           'or a sequence of space '
            }
            return JsonResponse(data, status=404)


# Класс для передачи данных о задачах с путём, в конце которого есть индекс(id) экземпляра сущности
@method_decorator(csrf_exempt, name='dispatch')
class TaskViewForIndexInEnd(View):

    # Метод для изменения задачи по id
    def put(self, request, task_id):
        if Task.objects.filter(task_id=task_id):
            task = Task.objects.get(task_id=task_id)

            put_body = json.loads(request.body)
            task_name = put_body.get('task_name')
            task_description = put_body.get('task_description')
            task_status = put_body.get('task_status')

            if task_name is not None:
                if is_correct_name(task_name):
                    task.task_name = task_name

                else:
                    data = {
                        'message': 'Task object has not been changed because task_name must not been a space or a sequence of space'
                    }
                    return JsonResponse(data, status=404)

            if task_description is not None:
                task.task_description = task_description

            if task_status is not None:
                if is_status(task_status):
                    task.task_status = task_status

                else:
                    data = {
                        'message': 'Task object has not been changed because status must been boolean type'
                    }
                    return JsonResponse(data, status=404)

            task.save()

            data = {
                'task_id': task.task_id,
                'task_name': task.task_name,
                'task_description': task.task_description,
                'task_status': task.task_status
            }
            return JsonResponse(data, status=200)

        else:
            data = {
                'message': 'Task did not find in database',
            }
            return JsonResponse(data, status=404)

    # Метод для удаления задачи
    def delete(self, request, task_id):

        if Task.objects.filter(task_id=task_id):
            task = Task.objects.get(task_id=task_id)

            task.delete()

            data = {
                'message': 'Success delete',
            }
            return JsonResponse(data, status=200)
        else:
            data = {
                'message': 'Task did not find in database'
            }
            return JsonResponse(data, status=404)

    # Метод для обновления статуса задачи
    def patch(self, request, task_id):
        if Task.objects.filter(task_id=task_id):
            task = Task.objects.get(task_id=task_id)

            patch_body = json.loads(request.body)
            task_status = patch_body.get('task_status')

            if task_status is not None:
                if is_status(task_status):
                    task.task_status = task_status
                    task.save()
                    data = {
                        'task_id': task.task_id,
                        'task_name': task.task_name,
                        'task_description': task.task_description,
                        'task_status': task.task_status
                    }
                    return JsonResponse(data, status=200)

                else:
                    data = {
                        'message': 'Task object has not been changed because status must been boolean type'
                    }
                    return JsonResponse(data, status=404)

            else:
                data = {
                    'message': 'Task object has not been patched because task_status is null (is none). It must '
                               'be True or False and task_name must not been a space or a sequence of space '
                }
                return JsonResponse(data, status=404)
        else:
            data = {
                'message': 'Task did not find in database'
            }
            return JsonResponse(data, status=404)
