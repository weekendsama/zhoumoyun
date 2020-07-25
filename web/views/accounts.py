from django.shortcuts import render, HttpResponse, redirect
from web.forms.accounts import RegisterModelForm, SendSmsForm, LoginSMSForm, LoginForm
from django.http import JsonResponse
from web import models


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
        phone_num = form.cleaned_data['phone_num']
        user_obj = models.UserModel.objects.filter(phone_num=phone_num).first()
        request.session['user_id'] = user_obj.id
        request.session.set_expiry(60*60*24*14)
        return JsonResponse({'status': True, 'data': '/'})
    return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    if request.method == 'GET':
        form = LoginForm(request)
        return render(request, 'web/login.html', {'form': form})
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        from django.db.models import Q
        user_obj = models.UserModel.objects.filter(Q(email=username) | Q(phone_num=username)).\
            filter(password=password).first()
        if user_obj:
            request.session['user_id'] = user_obj.id
            request.session.set_expiry(60*60*24*14)
            return redirect('index')
        form.add_error('username', '用户名或密码错误')
    return render(request, 'web/login.html', {'form': form})


def image_code(request):
    # 生成图片验证码
    from io import BytesIO
    from utils.image_code import check_code

    image_object, code = check_code()
    request.session['image_code'] = code
    request.session.set_expiry(60)
    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())
