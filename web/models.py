from django.db import models


# Create your models here.


class UserModel(models.Model):
    def __str__(self):
        return self.username

    username = models.CharField(verbose_name='用户名', max_length=16, db_index=True)  # db_index 创建索引
    email = models.EmailField(verbose_name='邮箱', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=32)
    phone_num = models.CharField(verbose_name='手机号', max_length=15)


class PricePolicy(models.Model):
    category_choices = ((1, '免费版'), (2, '收费版'), (3, '其他'))
    category = models.SmallIntegerField(verbose_name='收费类型', choices=category_choices, default=1)
    title = models.CharField('标题', max_length=32)
    price = models.PositiveIntegerField(verbose_name='价格')
    project_num = models.PositiveIntegerField(verbose_name='项目数')
    project_member = models.PositiveIntegerField(verbose_name='项目成员')
    project_space = models.PositiveIntegerField(verbose_name='单项目空间')
    per_file_size = models.PositiveIntegerField(verbose_name='单文件大小')
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Transaction(models.Model):
    """'交易记录"""
    status_code = (
        (1, '未支付'),
        (2, '已支付')
    )
    status = models.SmallIntegerField(verbose_name='状态', choices=status_code)
    order = models.CharField(verbose_name='订单号', max_length=64, unique=True)
    user = models.ForeignKey(verbose_name='用户', to='UserModel', on_delete=models.CASCADE)
    price_policy = models.ForeignKey(verbose_name='价格策略', to='PricePolicy', on_delete=models.CASCADE)
    count = models.IntegerField(verbose_name='数量（年）', help_text='0表示无限期')
    price = models.IntegerField(verbose_name='实际支付价格')
    start_datetime = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    end_datetime = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Project(models.Model):
    COLOR_CHOICE = (
        (1, '#56b8eb'),
        (2, '#f28033'),
        (3, '#ebc656'),
        (4, '#a2d148'),
        (5, '#7461c2'),
        (6, '#20bfa3')
    )

    name = models.CharField(verbose_name='项目名', max_length=32)
    color = models.SmallIntegerField(verbose_name='颜色', choices=COLOR_CHOICE, default=1)
    desc = models.CharField(verbose_name='项目描述', max_length=255, null=True, blank=True)
    used_space = models.IntegerField(verbose_name='项目已用空间', default=0)
    star = models.BooleanField(verbose_name='星标', default=False)
    join_count = models.SmallIntegerField(verbose_name='参与人数', default=1)
    creator = models.ForeignKey(verbose_name='创建者', to='UserModel', on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    bucket = models.CharField(verbose_name='COS桶', max_length=128)
    region = models.CharField(verbose_name='桶区域', max_length=32)


class ProjectUser(models.Model):
    user = models.ForeignKey(verbose_name='用户', to='UserModel', on_delete=models.CASCADE)
    project = models.ForeignKey(verbose_name='项目', to='Project', on_delete=models.CASCADE)
    invitee = models.ForeignKey(verbose_name='邀请者', to='UserModel', related_name='invites', null=True, blank=True,
                                on_delete=models.CASCADE)
    star = models.BooleanField(verbose_name='星标', default=False)
    create_time = models.DateTimeField(verbose_name='加入时间', auto_now_add=True)


class Wiki(models.Model):

    def __str__(self):
        return self.title

    project = models.ForeignKey(verbose_name='项目', to='Project', on_delete=models.CASCADE)
    title = models.CharField(verbose_name='标题', max_length=32)
    content = models.TextField(verbose_name='内容')
    parent = models.ForeignKey(verbose_name='父级文章', to='self', null=True, blank=True, on_delete=models.CASCADE,
                               related_name='children')
    depth = models.IntegerField(verbose_name='深度', default=1)


class FileRepository(models.Model):
    project = models.ForeignKey(verbose_name='项目名', to=Project, on_delete=models.CASCADE)
    file_type_choices = (
        (1, '文件'),
        (2, '文件夹')
    )
    file_type = models.SmallIntegerField(verbose_name='文件类型', choices=file_type_choices)
    name = models.CharField(verbose_name='文件名称', max_length=32, help_text='文件/文件夹名称')
    key = models.CharField(verbose_name='文件存储在cos中的KEY', max_length=128, null=True, blank=True)
    file_size = models.IntegerField(verbose_name='文件大小', null=True, blank=True)
    file_path = models.CharField(verbose_name='文件路径', max_length=255, null=True, blank=True)
    parent = models.ForeignKey(verbose_name='父级目录', to='self', related_name='child', on_delete=models.CASCADE,
                               null=True, blank=True)
    update_user = models.ForeignKey(verbose_name='更新者', to='UserModel', on_delete=models.CASCADE)
    update_datetime = models.DateTimeField(verbose_name='更新时间', auto_now=True)
