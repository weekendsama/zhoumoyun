from web import models
from django import forms
from web.forms.bootstrap import BootStrapForm


class WikiModelForm(BootStrapForm, forms.ModelForm):
    class Meta:
        model = models.Wiki
        exclude = ['project', 'depth']

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)

        total_data_list = [('', '无父级文章')]
        data_list = models.Wiki.objects.filter(project=request.auth.project).values_list('id', 'title')
        total_data_list.extend(data_list)
        self.fields['parent'].choices = total_data_list
