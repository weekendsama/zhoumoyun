from django.db import models

# Create your models here.


class TestBlogModel(models.Model):
    # 使得每个模型返回标题
    def __str__(self):
        return self.title
    # verbose_name指定显示名（label）
    author = models.CharField(verbose_name='作者', max_length=16)
    title = models.CharField(verbose_name='标题', max_length=32)
    body = models.TextField(verbose_name='文章主体')
    created_time = models.DateTimeField(verbose_name='创建时间')
    modified_time = models.DateTimeField(verbose_name='修改时间')





