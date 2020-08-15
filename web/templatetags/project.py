from django.template import Library
from web import models

register = Library()


@register.inclusion_tag('web/inclusion/all_project_list.html')
def all_project_list(request):
    my_list = models.Project.objects.filter(creator=request.auth.user)
    join_list = models.ProjectUser.objects.filter(user=request.auth.user)
    return {'mine': my_list, 'join': join_list}
