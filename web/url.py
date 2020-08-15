from django.urls import path, include
from web.views import accounts
from web.views import index
from web.views import project
from web.views import manage

app_name = 'web'
urlpatterns = [
    # 账户相关
    path('register/', accounts.register, name='register'),
    path('send/sms/', accounts.send_sms, name='send_sms'),
    path('login/sms/', accounts.login_sms, name='login_sms'),
    path('login/', accounts.login, name='login'),
    path('image/code/', accounts.image_code, name='image_code'),
    # 主页
    path('', index.home, name='home'),
    # 后台项目相关
    path('logout/', accounts.logout, name='logout'),
    path('project/list/', project.project_list, name='manage_center'),
    path('project/star/<str:project_type>/<int:project_id>/', project.project_star, name='project_star'),
    path('project/unstar/<str:project_type>/<int:project_id>/', project.project_un_star, name='project_un_star'),
    # 项目管理
    path('manage/<int:project_id>/', include([
        path('dashboard/', manage.dashboard, name='dashboard'),
        path('issues/', manage.issues, name='issues'),
        path('statistics/', manage.statistics, name='statistics'),
        path('file/', manage.file, name='file'),
        path('wiki/', manage.wiki, name='wiki'),
        path('settings/', manage.settings, name='settings'),
    ])),
]
