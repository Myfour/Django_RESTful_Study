from django.db import models


# Create your models here.
class TestModel(models.Model):
    name = models.CharField(max_length=20)
    code = models.TextField()
    created_time = models.DateTimeField(
        auto_now_add=True)  # 在新增这个对象时设置这个属性为当前时间
    changed_time = models.DateTimeField(auto_now=True)  # 每次修改这个对象都设置这个属性的当前时间

    def __str__(self):
        return self.name
