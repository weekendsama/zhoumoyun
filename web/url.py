from django.urls import path
from web.views import accounts
from web.views import index

app_name = 'web'
urlpatterns = [
    path('register/', accounts.register, name='register'),
    path('send/sms/', accounts.send_sms, name='send_sms'),
    path('login/sms/', accounts.login_sms, name='login_sms'),
    path('login/', accounts.login, name='login'),
    path('image/code/', accounts.image_code, name='image_code'),
    path('', index.home, name='home'),
]
