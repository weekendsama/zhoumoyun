from django.utils.deprecation import MiddlewareMixin
from web import models


class AuthMiddleWare(MiddlewareMixin):

    def process_request(self, request):
        # 用户登录后 request 中赋值
        user_id = request.session.get('user_id', 0)
        user_obj = models.UserModel.objects.filter(id=user_id).first()
        request.auth = user_obj
