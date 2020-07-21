from django.db import models

# Create your models here.


class TestBlogModel(models.Model):
    # 使得每个模型返回标题
    def __str__(self):
        return self.title

    author = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    body = models.TextField()
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()


