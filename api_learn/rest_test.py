from django import setup
import os
# 加载配置
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_learn.settings')
setup()