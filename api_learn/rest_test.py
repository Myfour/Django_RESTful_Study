from django import setup
import os
# 加载配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_learn.settings')
setup()  # 加载配置文件，通过寻找环境变量DJANGO_SETTINGS_MODULE的值来作为配置文件的路径

from rest_framework import serializers


# 类似于Django的Form的逻辑
class TestSerilOne(serializers.Serializer):  # DRF的序列化器双向验证
    name = serializers.CharField(max_length=20)
    age = serializers.IntegerField()


fontend_data = {'name': 'myfour', 'age': '22d'}

# 前端的数据验证
# test = TestSerilOne(data=fontend_data)

# if test.is_valid():
#     print(test.validated_data)
# else:
#     print(test.errors)  # 输出序列化器的错误信息


class TestSerilTwo(serializers.Serializer):
    name = serializers.CharField(max_length=20)


# 后端的数据验证
from rest_learn.models import TestModel

# code = TestModel.objects.get(name='ls')
# # test = TestSerilTwo(instance=code)  # instance传一个实例给序列化器
# codes = TestModel.objects.all()

# print(code)
# print(codes)


# test = TestSerilTwo(instance=codes, many=True)  # many参数告诉序列化器传入的是一个结果集
# print(test.data)
class TestSerilThree(serializers.ModelSerializer):
    class Meta:
        model = TestModel
        fields = ['name', 'code', 'created_time', 'changed_time', 'id']
        read_only_fields = ['created_time', 'changed_time']


# 前端写入测试
# fontend_data = {
#     'name': 'ModelSeril',
#     'code': '''print("frontend test")''',
#     'created_time': '2017-12-16'
# }
# test1 = TestSerilThree(data=fontend_data)
# if test1.is_valid():
#     print('Frontend test:', test1.validated_data)

# 后端输出测试
# test2 = TestSerilThree(instance=code)
# print('Backend single instance test:', test2.data)
# test3 = TestSerilThree(instance=codes, many=True)
# print('Backend multiple instance test:', test3.data)


class ProfileSerializer(serializers.Serializer):
    tel = serializers.CharField(max_length=15)
    height = serializers.IntegerField()


class UserSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=20)
    qq = serializers.CharField(max_length=15)
    profile = ProfileSerializer()


# 外键关系的前端输入测试
# frontend_data = {
#     'name': 'myfour',
#     'qq': '913906842',
#     'profile': {
#         'tel': '12342321234',
#         'height': '180'
#     }
# }
# test = UserSerializer(data=frontend_data)
# if test.is_valid():
#     print(test.validated_data)

# 自定义一个字段
# class TEL(object):
#     def __init__(self, num=None):
#         self.num = num

#     def text(self, message):
#         """发短信功能"""
#         return self._send_message(message)

#     def _send_message(self, message):
#         """发短信"""
#         print('Send {} to {}'.format(message[:10], self.num))

# class TELField(serializers.Field):
#     def to_representation(self, tel_obj):
#         return tel_obj.num

#     def to_internal_value(self, data):
#         data = data.lstrip().rstrip().strip()
#         if 8 <= len(data) <= 11:
#             return TEL(data)
#         raise serializers.ValidationError('Invalid telephone number.')

from rest_framework.viewsets import ModelViewSet


class TestViewSet(ModelViewSet):
    queryset = TestModel.objects.all()


from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'codes', TestViewSet)
urlpatterns = router.urls
print(urlpatterns)
