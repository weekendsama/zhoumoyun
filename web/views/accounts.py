from django.shortcuts import render
from web.forms.accounts import RegisterModelForm, SendSmsForm
from django.http import JsonResponse


def register(request):
    form = RegisterModelForm()
    return render(request, 'web/register.html', {'form': form})


def send_sms(request):
    """
    发送短信
    """

    form = SendSmsForm(request, data=request.GET)
    # 校验成功后
    if form.is_valid():
        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})

