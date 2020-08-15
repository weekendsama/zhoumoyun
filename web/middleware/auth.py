import datetime
from django.utils.deprecation import MiddlewareMixin
from web import models
from django.conf import settings
from django.shortcuts import redirect


class Auth(object):
    def __init__(self):
        self.user = None
        self.price_policy = None
        self.project = None


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        # 用户登录后 request 中赋值
        request.auth = Auth()
        user_id = request.session.get('user_id', 0)
        user_obj = models.UserModel.objects.filter(id=user_id).first()
        request.auth.user = user_obj
        if request.path_info not in settings.BLACK_URL_LIST:
            return None
        if not request.auth.user:
            return redirect('web:login')

        obj = models.Transaction.objects.filter(user=user_obj, status=2).order_by('-id').first()
        current_datetime = datetime.datetime.now()
        if obj.end_datetime and obj.end_datetime < current_datetime:
            obj = models.Transaction.objects.filter(user=user_obj, status=2, price_policy__category=1).first()
        request.auth.price_policy = obj.price_policy

    def process_view(self, request, view, args, kwargs):
        if not request.path_info.startswith('/manage/'):
            return None
        project_id = kwargs.get('project_id')
        project_obj = models.Project.objects.filter(creator=request.auth.user, id=project_id).first()
        if project_obj:
            request.auth.project = project_obj
            return None

        project_user_obj = models.ProjectUser.objects.filter(user=request.auth.user, project_id=project_id).first()
        if project_user_obj:
            request.auth.project = project_user_obj.project
            return None
        return redirect('web:manage_center')
