import random
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from web import models
from django.conf import settings
from utils.tencent.sms import send_sms_single
from utils import encrypt


class RegisterModelForm(forms.ModelForm):
    phone_num = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    password = forms.CharField(label='密码',
                               min_length=8,
                               max_length=32,
                               error_messages={
                                   'min_length': '密码长度不能少于8个字符',
                                   'max_length': '密码长度不能长于32个字符',
                               },
                               widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='重复密码',
                                       min_length=8,
                                       max_length=32,
                                       error_messages={
                                           'min_length': '重复密码长度不能少于8个字符',
                                           'max_length': '重复密码长度不能长于32个字符',
                                       },
                                       widget=forms.PasswordInput())
    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserModel
        fields = ['username', 'email', 'password', 'confirm_password', 'phone_num', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入{}'.format(field.label)

    def clean_username(self):
        username = self.cleaned_data['username']

        exists = models.UserModel.objects.filter(username=username).exists()
        if exists:
            raise ValidationError('用户名已存在')

        return username

    def clean_email(self):
        email = self.cleaned_data['email']

        exists = models.UserModel.objects.filter(email=email).exists()
        if exists:
            raise ValidationError('邮箱已存在')

        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        # 加密并返回
        return encrypt.md5(password)

    def clean_confirm_password(self):
        password = encrypt.md5(self.cleaned_data['password'])
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('两次密码不一致')

        return confirm_password

    def clean_phone_num(self):
        phone_num = self.cleaned_data['phone_num']
        exists = models.UserModel.objects.filter(phone_num=phone_num).exists()
        if exists:
            raise ValidationError('手机号已注册')
        return phone_num


"""    def clean_code(self):
        code = self.cleaned_data['code']
        phone_num = self.cleaned_data['phone_num']
        
        pass"""


class SendSmsForm(forms.Form):
    phone_num = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_phone_num(self):
        """手机号校验钩子 """
        phone_num = self.cleaned_data['phone_num']

        # 判断短信模板有没有问题
        tpl = self.request.GET.get('tpl')
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            raise ValidationError('模板错误')
        # 校验数据库已有手机号
        exists = models.UserModel.objects.filter(phone_num=phone_num).exists()
        if exists:
            raise ValidationError('手机号存在')
        # 发短信
        code = random.randrange(1000, 9999)
        sms = send_sms_single(phone_num, template_id, [code, ])
        if sms['result'] != 0:
            raise ValidationError('短信发送失败, {}'.format(sms['errmsg']))
        # 写入redis

        return phone_num
