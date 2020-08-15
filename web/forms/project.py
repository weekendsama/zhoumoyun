from django import forms
from web.forms.bootstrap import BootStrapForm
from web import models
from django.core.exceptions import ValidationError
from web.forms.widgets import ColorRadioSelect


class ProjectModelForm(BootStrapForm, forms.ModelForm):
    bootstrap_class_exclude = ['color']

    class Meta:
        model = models.Project
        fields = ['name', 'color', 'desc']
        widgets = {
            'desc': forms.Textarea,
            'color': ColorRadioSelect(attrs={'class': 'color-radio'})
        }

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_name(self):
        # 项目校验
        name = self.cleaned_data['name']
        exists = models.Project.objects.filter(name=name, creator=self.request.auth.user).exists()
        if exists:
            raise ValidationError('项目名已存在')
        count = models.Project.objects.filter(creator=self.request.auth.user).count()
        if count >= self.request.auth.price_policy.project_num:
            raise ValidationError('项目已超限，请升级账户')
        return name
