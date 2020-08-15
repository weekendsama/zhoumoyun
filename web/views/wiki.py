from django.shortcuts import render, redirect, reverse
from web.forms.wiki import WikiModelForm


def wiki(request, project_id):
    return render(request, 'web/wiki.html')


def wiki_add(request, project_id):
    if request.method == 'GET':
        form = WikiModelForm(request)
        return render(request, 'web/wiki_add.html', {'form': form})
    form = WikiModelForm(request, data=request.POST)
    if form.is_valid():
        form.instance.project = request.auth.project
        form.save()
        url = reverse('web:wiki', kwargs={'project_id': project_id})
        return redirect(url)
    return render(request, 'web/wiki_add.html', {'form': form})
