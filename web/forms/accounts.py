import random
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from web import models
from django.conf import settings
from utils.tencent.sms import send_sms_single


class RegisterModelForm(forms.ModelForm):
    phone_num = forms.CharField(label='手机号', validators=[RegexValidator(r'^(1[3|4|5|6|7|8|9])\d{9}$', '手机号格式错误'), ])
    password = forms.CharField(label='密码', widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='重复密码', widget=forms.PasswordInput())
    code = forms.CharField(label='验证码')

    class Meta:
        model = models.UserModel
        fields = ['username', 'email', 'password', 'confirm_password', 'phone_num', 'code']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入{}'.format(field.label)


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
