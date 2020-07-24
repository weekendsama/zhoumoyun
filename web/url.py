from django.urls import path
from web.views import accounts

app_name = 'web'
urlpatterns = [
    path('register/', accounts.register, name='register'),
]
