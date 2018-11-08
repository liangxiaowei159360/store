'''
author:梁晓伟
datetime:2018/11/6 20:06
Desc: urls
'''
from django.conf.urls import url


from . import views


urlpatterns = [
    url(r"^users_register/", views.users_register, name="users_register"),
    url(r"^users_login/", views.users_login, name="users_login"),
    url(r"^users_update/", views.users_update, name="users_update"),
]