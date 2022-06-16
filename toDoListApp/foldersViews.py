# API for folder model

import json

from django.core.serializers import serialize
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from .models import Folder
from .validators import *


# Класс для передачи данных о папках с путём без индекса(id) экземпляра сущности в конце
@method_decorator(csrf_exempt, name='dispatch')
class FolderView(View):

    # Метод для получения всех папок
    def get(self, request):

        folders = Folder.objects.all()

        task_serialized_data = serialize('python', folders)

        count_of_instance = Folder.objects.count()

        instance_output_list_of_dicts = list(dict())
        for i in range(count_of_instance):
            folder_id = task_serialized_data[i]['pk']
            fields_task_dict = task_serialized_data[i]['fields']
            fields_task_dict['folder_id'] = folder_id
            instance_output_list_of_dicts.append({'folder_id': folder_id,
                                                  'folder_name': fields_task_dict['folder_name'],
                                                  'parent_folder': fields_task_dict['parent_folder'],
                                                  })

        output_data = {
            "folders": instance_output_list_of_dicts
        }

        return JsonResponse(output_data, safe=False)

    # Метод для создания папки
    def post(self, request):

        post_body = json.loads(request.body)

        folder_name = post_body.get('folder_name')
        parent_folder = post_body.get('parent_folder')

        folder_data = dict()

        if parent_folder is None:
            folder_data = {
                'folder_name': folder_name,
                'parent_folder': None
            }

        elif Folder.objects.filter(folder_id=parent_folder):
            folder_data = {
                'folder_name': folder_name,
                'parent_folder': Folder.objects.get(folder_id=parent_folder),
            }

        else:
            data = {
                'message': 'New folder object has not been created because parent_folder is not exist'
            }
            return JsonResponse(data, status=404)

        if folder_name is not None:
            if is_correct_name(folder_name):
                folder_object = Folder.objects.create(**folder_data)
                folder_object.save()
                data = dict()

                if folder_object.parent_folder is None:
                    data = {
                        'folder_id': folder_object.folder_id,
                        'folder_name': folder_object.folder_name,
                        'parent_folder': folder_object.parent_folder,
                    }

                else:
                    data = {
                        'folder_id': folder_object.folder_id,
                        'folder_name': folder_object.folder_name,
                        'parent_folder': folder_object.parent_folder.folder_id,
                    }

                return JsonResponse(data, status=201)

            else:
                data = {
                    'message': 'New folder object has not been created because folder_name must not been a space or a '
                               'sequence of space ',
                }
                return JsonResponse(data, status=404)

        else:
            data = {
                'message': 'New folder object has not been created because folder_name must not been a null value',
            }
            return JsonResponse(data, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class FolderViewForIndexInEnd(View):

    # Метод для обновления названия папки
    def patch(self, request, folder_id):
        if Folder.objects.filter(folder_id=folder_id):
            folder = Folder.objects.get(folder_id=folder_id)

            patch_body = json.loads(request.body)
            folder_name = patch_body.get('folder_name')

            if folder_name is not None:

                if is_correct_name(folder_name):
                    folder.folder_name = folder_name
                    folder.save()
                    data = dict()

                    if folder.folder_id is None:
                        data = {
                            'folder_id': folder.folder_id,
                            'folder_name': folder.folder_name,
                            'parent_folder': folder.parent_folder
                        }

                    else:
                        data = {
                            'folder_id': folder.folder_id,
                            'folder_name': folder.folder_name,
                            'parent_folder': folder.parent_folder.folder_id
                        }
                    return JsonResponse(data, status=200)

                else:
                    data = {
                        'message': 'Folder object has not been patched because folder name must must not been a space or a sequence of space'
                    }
                    return JsonResponse(data, status=404)

            else:
                data = {
                    'message': 'Folder object has not been patched because folder name is null (is none)'
                }
                return JsonResponse(data, status=404)

        else:
            data = {
                'message': 'Folder did not find in database'
            }
            return JsonResponse(data, status=404)

    # Метод для удаления папки
    def delete(self, request, folder_id):

        if Folder.objects.filter(folder_id=folder_id):
            folder = Folder.objects.get(folder_id=folder_id)

            folder.delete()

            data = {
                'message': 'Success delete',
            }
            return JsonResponse(data, status=200)

        else:
            data = {
                'message': 'Folder did not find in database'
            }
            return JsonResponse(data, status=404)
