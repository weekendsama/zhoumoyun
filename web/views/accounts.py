import uuid
import datetime
from django.utils import timezone
from django.shortcuts import render, HttpResponse, redirect
from web.forms.accounts import RegisterModelForm, SendSmsForm, LoginSMSForm, LoginForm
from django.http import JsonResponse
from web import models
from io import BytesIO
from utils.image_code import check_code
from django.db.models import Q


def register(request):
    # GET方法进入`register`页面
    if request.method == 'GET':
        form = RegisterModelForm()
        return render(request, 'web/register.html', {'form': form})
    # POST方法接收表单
    form = RegisterModelForm(data=request.POST)
    if form.is_valid():
        instance = form.save()
        policy_obj = models.PricePolicy.objects.filter(category=1, title='个人免费版').first()
        models.Transaction.objects.create(
            status=2,
            order=str(uuid.uuid4()),
            user=instance,
            price_policy=policy_obj,
            count=0,
            price=0,
            start_datetime=datetime.datetime.now(tz=timezone.utc)
        )

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
        request.session.set_expiry(60 * 60 * 24 * 14)
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
        user_obj = models.UserModel.objects.filter(Q(email=username) | Q(phone_num=username)). \
            filter(password=password).first()
        if user_obj:
            request.session['user_id'] = user_obj.id
            request.session.set_expiry(60 * 60 * 24 * 14)
            return redirect('web:home')
        form.add_error('username', '用户名或密码错误')
    return render(request, 'web/login.html', {'form': form})


def image_code(request):
    # 生成图片验证码

    image_object, code = check_code()
    request.session['image_code'] = code
    request.session.set_expiry(60)
    stream = BytesIO()
    image_object.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect('web:home')
