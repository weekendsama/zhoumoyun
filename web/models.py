from django.db import models

# Create your models here.


class UserModel(models.Model):
    def __str__(self):
        return self.username

    username = models.CharField(verbose_name='用户名', max_length=16, db_index=True)  # db_index 创建索引
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    phone_num = models.CharField(verbose_name='手机号', max_length=15)
