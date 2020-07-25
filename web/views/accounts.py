from django.shortcuts import render
from web.forms.accounts import RegisterModelForm, SendSmsForm, LoginSMSForm
from django.http import JsonResponse


def register(request):
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'web/register.html', {'form': form})

    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': True, 'data': '/login/'})
    return JsonResponse({'status': False, 'error': form.errors})


def send_sms(request):
    """
    发送短信
    """

    form = SendSmsForm(request, data=request.GET)
    # 校验成功后
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    if request.method == 'GET':
        form = LoginSMSForm()
        return render(request, 'web/login_sms.html', {'form': form})
    form = LoginSMSForm(request.POST)
    if form.is_valid():
        return JsonResponse({'status': True, 'data': '/index/'})
    return JsonResponse({'status': False, 'error': form.errors})
