# -*- coding: utf-8 -*
from fabric import task

# from invoke import Responder
# from _credentials import github_username, github_password


# def _get_github_auth_responders():
#     """
#     返回 GitHub 用户名密码自动填充器
#     """
#     username_responder = Responder(
#         pattern="Username for 'https://github.com':",
#         response='{}\n'.format(github_username)
#     )
#     password_responder = Responder(
#         pattern="Password for 'https://{}@github.com':".format(github_username),
#         response='{}\n'.format(github_password)
#     )
#     return [username_responder, password_responder]
def virtualenv_(c, source, cmd):
    c.run(source + cmd)


@task()
def deploy(c):
    supervisor_conf_path = '/root/etc'
    supervisor_program_name = 'mystore'
    project_root_path = '/home/sites/MyStore'
    source = 'source /home/sites/MyStore/env/bin/activate && '

    # 先停止应用
    with c.cd(supervisor_conf_path):
        cmd = 'supervisorctl stop {}'.format(supervisor_program_name)
        c.run(cmd)

    # 进入项目根目录，从 Git 拉取最新代码
    with c.cd(project_root_path):
        cmd = 'git pull'
        # responders = _get_github_auth_responders()
        # c.run(cmd, watchers=responders)

    # 安装依赖，迁移数据库，收集静态文件
    with c.cd(project_root_path):
        virtualenv_(c, source, 'pip install -r requirements/production.txt')
        virtualenv_(c, source, 'python manage.py makemigrations')
        virtualenv_(c, source, 'python manage.py migrate')
        virtualenv_(c, source, 'python manage.py collectstatic --noinput')

    # 重新启动 nginx
    c.run('sudo service nginx reload')

    # 重新启动应用
    with c.cd(supervisor_conf_path):
        cmd = 'supervisorctl start {}'.format(supervisor_program_name)
        c.run(cmd)
