from django.shortcuts import render, HttpResponse, redirect
from web.forms.project import ProjectModelForm
from django.http import JsonResponse
from web import models
from utils.tencent.cos import create_bucket
import time


def project_list(request):
    if request.method == 'GET':
        form = ProjectModelForm(request)

        project_dict = {'star': [], 'mine': [], 'joined': []}
        raw_project_list = models.Project.objects.filter(creator=request.auth.user)
        for item in raw_project_list:
            if item.star:
                project_dict['star'].append({'value': item, 'type': 'mine'})
            else:
                project_dict['mine'].append(item)
        raw_join_list = models.ProjectUser.objects.filter(user=request.auth.user)
        for item in raw_join_list:
            if item.star:
                project_dict['star'].append({'value': item.project, 'type': 'joined'})
            else:
                project_dict['joined'].append(item.project)

        return render(request, 'web/project_list.html', {'form': form, 'project_dict': project_dict})

    form = ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        # 创建桶与区域
        bucket = '{}-{}-1302697284'.format(request.auth.user.phone_num,
                                           str(int(time.time() * 1000)))
        region = 'ap-nanjing'
        create_bucket(bucket, region)
        form.instance.region = region
        form.instance.bucket = bucket
        form.instance.creator = request.auth.user
        form.save()
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_type, project_id):
    if project_type == 'mine':
        models.Project.objects.filter(id=project_id, creator=request.auth.user).update(star=True)
        return redirect('web:manage_center')
    if project_type == 'joined':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.auth.user).update(star=True)
        return redirect('web:manage_center')

    return HttpResponse('请求错误')


def project_un_star(request, project_type, project_id):
    if project_type == 'mine':
        models.Project.objects.filter(id=project_id, creator=request.auth.user).update(star=False)
        return redirect('web:manage_center')
    if project_type == 'joined':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.auth.user).update(star=False)
        return redirect('web:manage_center')

    return HttpResponse('请求错误')
