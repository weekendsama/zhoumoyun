from django.shortcuts import render
from django.http import JsonResponse
from web.forms.file import FolderModelForm
from django.forms import model_to_dict
from web import models
from utils.tencent.cos import delete_file, delete_file_list


def file(request, project_id):
    parent_object = None
    folder_id = request.GET.get('folder', '')
    if folder_id.isdecimal():
        parent_object = models.FileRepository.objects.filter(
            id=int(folder_id),
            file_type=2,
            project=request.auth.project,
        ).first()
    # GET显示页面
    if request.method == 'GET':
        breadcrumb_list = []
        parent = parent_object
        while parent:
            breadcrumb_list.insert(0, model_to_dict(parent, ['id', 'name']))
            parent = parent.parent
        queryset = models.FileRepository.objects.filter(project=request.auth.project)
        if parent_object:
            file_object_list = queryset.filter(parent=parent_object).order_by('-file_type')
        else:
            file_object_list = queryset.filter(parent__isnull=True).order_by('-file_type')
        form = FolderModelForm(request, parent_object)
        context = {
            'form': form,
            'file_object_list': file_object_list,
            'breadcrumb_list': breadcrumb_list
        }
        return render(request, 'web/file.html', context)

    # POST 发送请求
    fid = request.POST.get('fid', '')
    edit_object = None
    if fid.isdecimal():
        edit_object = models.FileRepository.objects.filter(id=int(fid), file_type=2,
                                                           project=request.auth.project).first()
    if edit_object:
        form = FolderModelForm(request, parent_object, data=request.POST, instance=edit_object)
    else:
        form = FolderModelForm(request, parent_object, data=request.POST)

    if form.is_valid():
        form.instance.project = request.auth.project
        form.instance.file_type = 2
        form.instance.update_user = request.auth.user
        form.instance.parent = parent_object
        form.save()
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def file_delete(request, project_id):
    fid = request.GET.get('fid')
    delete_object = models.FileRepository.objects.filter(id=int(fid), project=request.auth.project).first()
    if delete_object.file_type == 1:
        # 删除文件，返还使用空间
        request.auth.project.used_space -= delete_object.file_size
        request.auth.project.save()
        # cos操作删除文件
        delete_file(request.auth.project.bucket, request.auth.project.region, delete_object.key)
        # 数据库中删除
        delete_object.delete()
        return JsonResponse({'status': True})
    total_size = 0
    key_list = []
    folder_list = [delete_object, ]
    for folder in folder_list:
        child_list = models.FileRepository.objects.filter(project=request.auth.project, parent=folder).order_by(
            '-file_type')
        for child in child_list:
            if child.file_type == 2:
                folder_list.append(child)
            else:
                total_size += child.file_size
                key_list.append({'Key': child.key})
    if key_list:
        delete_file_list(request.auth.project.bucket, request.auth.project.region, key_list)
    if total_size:
        request.auth.project.used_space -= total_size
        request.auth.project.save()
    delete_object.delete()
    return JsonResponse({'status': True})
