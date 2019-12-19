from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = "用户管理"


# bug: xamdin 用户名和密码正确，但登录不了，信号量的问题
# fixbug： 注释掉所有关于信号量
    def ready(self):
        import users.signals