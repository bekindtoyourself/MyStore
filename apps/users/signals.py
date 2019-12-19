# -*- coding: utf-8 -*-
__author__ = 'bobby'

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token

User = get_user_model()

# bug: xamdin 用户名和密码正确，但登录不了，信号量的问题
# fixbug： 注释掉所有关于信号量
@receiver(post_save, sender=User)
def create_user(sender, instance=None, created=False, **kwargs):
    if created:
        password = instance.password
        instance.set_password(password)
        instance.save()
