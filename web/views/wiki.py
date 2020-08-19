from django.shortcuts import render, redirect, reverse
from web.forms.wiki import WikiModelForm
from django.http import JsonResponse
from web import models
from django.views.decorators.csrf import csrf_exempt
from utils.encrypt import uid
from utils.tencent.cos import upload_file


def wiki(request, project_id):
    wiki_id = request.GET.get('wiki_id')
    if not wiki_id or not wiki_id.isdecimal():
        return render(request, 'web/wiki.html')
    wiki_obj = models.Wiki.objects.filter(id=wiki_id, project=request.auth.project).first()
    return render(request, 'web/wiki.html', {'wiki_object': wiki_obj})


def wiki_add(request, project_id):
    if request.method == 'GET':
        form = WikiModelForm(request)
        return render(request, 'web/wiki_form.html', {'form': form})
    form = WikiModelForm(request, data=request.POST)
    if form.is_valid():
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1
        form.instance.project = request.auth.project
        form.save()
        url = reverse('web:wiki', kwargs={'project_id': project_id})
        return redirect(url)
    return render(request, 'web/wiki_form.html', {'form': form})


def wiki_catalog(request, project_id):
    data = models.Wiki.objects.filter(project_id=project_id).values('id', 'title', 'parent_id').order_by('depth', 'id')
    return JsonResponse({'status': True, 'data': list(data)})


def wiki_delete(request, project_id, wiki_id):
    models.Wiki.objects.filter(project_id=project_id, id=wiki_id).delete()
    url = reverse('web:wiki', kwargs={'project_id': project_id})
    return redirect(url)


def wiki_edit(request, project_id, wiki_id):
    wiki_obj = models.Wiki.objects.filter(project_id=project_id, id=wiki_id).first()
    if not wiki_obj:
        url = reverse('web:wiki', kwargs={'project_id': project_id})
        return redirect(url)
    if request.method == 'GET':
        form = WikiModelForm(request, instance=wiki_obj)
        return render(request, 'web/wiki_form.html', {'form': form})
    form = WikiModelForm(request, data=request.POST, instance=wiki_obj)
    if form.is_valid():
        if form.instance.parent:
            form.instance.depth = form.instance.parent.depth + 1
        else:
            form.instance.depth = 1
        form.save()
        url = reverse('web:wiki', kwargs={'project_id': project_id})
        preview_url = '{}?wiki_id={}'.format(url, wiki_id)
        return redirect(preview_url)
    return render(request, 'web/wiki_form.html', {'form': form})


@csrf_exempt
def wiki_upload(request, project_id):
    result = {
        'success': 0,
        'message': None,
        'url': None
    }
    img_obj = request.FILES.get('editormd-image-file')
    if not img_obj:
        result['message'] = '文件不存在'
        return JsonResponse(result)
    ext = img_obj.name.rsplit('.')[-1]
    key = '{}.{}'.format(uid(request.auth.user.phone_num), ext)
    img_url = upload_file(
        request.auth.project.bucket,
        request.auth.project.region,
        img_obj,
        key
    )
    result['success'] = 1
    result['url'] = img_url
    return JsonResponse(result)

