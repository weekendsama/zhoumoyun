from django.shortcuts import render, HttpResponse


def dashboard(request, project_id):
    return render(request, 'web/dashboard.html')


def issues(request, project_id):
    pass


def statistics(request, project_id):
    pass


def file(request, project_id):
    pass


def wiki(request, project_id):
    pass


def settings(request, project_id):
    pass
