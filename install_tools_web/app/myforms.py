from django.forms import forms
from django import forms
from app import models
import re

class HostForm(forms.Form):
    host = forms.CharField(label="host", min_length=3, max_length=32,
                             error_messages={
                                 "required": "host不能为空",
                                 "invalid": "host格式不正确",
                             },
                             widget=forms.widgets.TextInput(attrs={"class": "form-control"})
                             )


    port = forms.CharField(label="端口",
                             error_messages={
                                 "required": "端口不能为空",
                                 "invalid": "端口只能是数字",
                             },
                           widget=forms.widgets.TextInput(attrs={"class": "form-control"})

                           )

    username = forms.CharField(label="用户名", min_length=3, max_length=8,
                               error_messages={
                                   "required": "用户名不能为空",
                                   "min_length": "用户名最小3位",
                                   "max_length": "用户名最大8位",
                               },
                               widget=forms.widgets.TextInput(attrs={"class": "form-control"})
                               )

    password = forms.CharField(label="密码", min_length=3, max_length=8,
                               error_messages={
                                   "required": "密码不能为空",
                                   "min_length": "密码最小3位",
                                   "max_length": "密码最大8位",
                               },
                               widget=forms.widgets.TextInput(attrs={"class": "form-control"})
                               )

    def clean_host(self):
        host = self.cleaned_data.get("host")
        pt = re.compile("^((2[0-4]\d|25[0-5]|[01]?\d\d?)\.){3}(2[0-4]\d|25[0-5]|[01]?\d\d?)$")
        res = pt.match(host)
        if not res:
            self.add_error("host", "host格式不正确")
        return host


class Regform(forms.Form):
    username = forms.CharField(label="用户名", min_length=3, max_length=8,
                               error_messages={
                                   "required": "用户名不能为空",
                                   "min_length": "用户名最小3位",
                                   "max_length": "用户名最大8位",
                               },
                               widget=forms.widgets.TextInput(attrs={"class": "form-control"})
                               )

    password = forms.CharField(label="密码", min_length=3, max_length=8,
                               error_messages={
                                   "required": "密码不能为空",
                                   "min_length": "密码最小3位",
                                   "max_length": "密码最大8位",
                               },
                               widget=forms.widgets.PasswordInput(attrs={"class": "form-control"})
                               )

    re_password = forms.CharField(label="确认密码", min_length=3, max_length=8,
                                  error_messages={
                                      "required": "确认密码不能为空",
                                      "min_length": "确认密码最小3位",
                                      "max_length": "确认密码最大8位",
                                  },
                                  widget=forms.widgets.PasswordInput(attrs={"class": "form-control"})
                                  )
    email = forms.EmailField(label="邮箱", min_length=3, max_length=32,
                             error_messages={
                                 "required": "邮箱不能为空",
                                 "invalid": "邮箱格式不正确",
                             },
                             widget=forms.widgets.EmailInput(attrs={"class": "form-control"})
                             )

    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_exist = models.UserInfo.objects.filter(username=username)
        if is_exist:
            self.add_error("username", "用户名已存在")
        return username

    def clean(self):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        if not password == re_password:
            self.add_error("re_password", "两次密码输入不一致")
        return self.cleaned_data


class Shellform(forms.Form):
    name = forms.CharField(label="shell脚本名称", min_length=1, max_length=200,
                               error_messages={
                                   "required": "shell名称不能为空",
                                   "min_length": "shell名称最小1位",
                                   "max_length": "shell名称最大10位",
                               },
                               widget=forms.widgets.TextInput(attrs={"class": "form-control"})
                               )

