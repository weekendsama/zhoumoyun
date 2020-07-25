from django.urls import path
from web.views import accounts

app_name = 'web'
urlpatterns = [
    path('register/', accounts.register, name='register'),
    path('send/sms/', accounts.send_sms, name='send_sms'),
    path('login/sms/', accounts.login_sms, name='login_sms'),
]
