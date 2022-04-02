import os
import threading
from itertools import count
from django.forms.models import model_to_dict
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from app.myforms import HostForm, Regform, Shellform
from app import models
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO, StringIO
from django.contrib import auth
import json
import random
# Create your views here.
from app.utils.create_code import create_validate_code
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.db import transaction
from app.utils.paramiko_to_shell import paramiko_uploadfile_to_linux,upfile_to_linux


def home(request):
    return render(request, 'home.html', locals())


def list(request):
    host_ls = models.Hosts.objects.filter().values('host', "pk").all()
    tool_ls = models.Shells.objects.filter().values("name", "pk").all()
    host_obj = HostForm()
    shellform_obj = Shellform()
    return render(request, 'list.html', locals())


def register(request):
    regform_obj = Regform()
    if request.method == "POST":
        if request.is_ajax():
            back_dic = {}
            formobj = Regform(request.POST)
            if formobj.is_valid():
                back_dic = {"code": 1000, 'msg': "注册成功"}
                clean_data = formobj.cleaned_data
                clean_data.pop("re_password")
                file_obj = request.FILES.get("avatar")
                if file_obj:
                    clean_data["avatar"] = file_obj
                models.UserInfo.objects.create_user(**clean_data)
                back_dic['url'] = '/app/login/'
            else:
                back_dic['code'] = 1001
                back_dic['msg'] = formobj.errors
            return JsonResponse(back_dic)

    return render(request, 'register.html', locals())


def login(request):
    if request.method == 'POST':
        back_dic = {"code": 1000, "mas": ""}
        username = request.POST.get("username")
        password = request.POST.get("password")
        code = request.POST.get("code")
        if request.session.get("code").lower() == code.lower():
            user_obj = auth.authenticate(username=username, password=password)
            if user_obj:
                auth.login(request, user_obj)
                back_dic["url"] = "/app/list"
                back_dic["msg"] = "登入成功"
            else:
                back_dic["code"] = 1002
                back_dic["msg"] = "用户名或者密码错误"
        else:
            back_dic["code"] = 1001
            back_dic["msg"] = "验证码错误"
        return JsonResponse(back_dic)
    return render(request, 'login.html', locals())


def logout(request):
    return redirect('login')


def get_code(request):
    img_obj, code = create_validate_code(font_path='static/font/111.ttf')
    request.session["code"] = code
    io_obj = BytesIO()
    img_obj.save(io_obj, 'png')
    return HttpResponse(io_obj.getvalue())


@login_required
def changepsd(request):
    if request.is_ajax():
        if request.method == 'POST':
            back_dic = {}
            oldpsd = request.POST.get("oldpsd")
            newpsd = request.POST.get("newpsd")
            sedpsd = request.POST.get("sedpsd")

            is_right = request.user.check_password(oldpsd)
            if is_right:
                if newpsd == sedpsd:
                    request.user.set_password(newpsd)
                    request.user.save()

                    back_dic["code"] = 1000
                    back_dic["msg"] = "修改成功"
                else:
                    back_dic["code"] = 1001
                    back_dic["msg"] = "两次密码输入不一致"
            else:
                back_dic["code"] = 1002
                back_dic["msg"] = "密码输入错误"
            return JsonResponse(back_dic
                                )
    return render(request, 'changepsd.html', locals())


def addhost(request):
    if request.is_ajax():
        back_dic = {}
        formobj = HostForm(request.POST)
        if formobj.is_valid():
            back_dic = {"code": 1000, 'msg': "添加成功"}
            clean_data = formobj.cleaned_data
            models.Hosts.objects.create(**clean_data)
            back_dic['url'] = '/app/list/'
        else:
            back_dic['code'] = 1001
            back_dic['msg'] = formobj.errors
        return JsonResponse(back_dic)
    return render(request, 'list.html', locals())


def addshell(request):
    if request.method == "POST":
        if request.is_ajax():
            back_dic = {}
            formobj = Shellform(request.POST)
            if formobj.is_valid():
                back_dic = {}
                clean_data = formobj.cleaned_data
                file_obj = request.FILES.get("shellfile")
                if file_obj:
                    if file_obj.name.endswith(".sh"):
                        clean_data["path"] = file_obj
                        models.Shells.objects.create(**clean_data)
                        back_dic["msg"] = "添加脚本成功"
                        back_dic['url'] = '/app/list/'
                    else:
                        back_dic['code'] = 1002
                        back_dic["msg"] = "请上传shell脚本文件"

            else:
                back_dic['code'] = 1001
                back_dic['msg'] = formobj.errors
            return JsonResponse(back_dic)
    return render(request, 'list.html', locals())


def delhost(request):
    if request.method == "POST":
        if request.is_ajax():
            back_dic = {}
            host_pk = request.POST.get("pk")
            res = models.Hosts.objects.filter(id=int(host_pk)).delete()
            if res:
                back_dic = {"code": 1000, 'msg': "删除成功"}
                back_dic['url'] = '/app/list/'
            else:
                back_dic['code'] = 1001
                back_dic['msg'] = "删除失败"

            return JsonResponse(back_dic)


def delshell(request):
    if request.method == "POST":
        if request.is_ajax():
            back_dic = {}
            shell_pk = request.POST.get("pk")
            res = models.Shells.objects.filter(id=int(shell_pk)).delete()
            if res:
                back_dic = {"code": 1000, 'msg': "删除成功"}
                back_dic['url'] = '/app/list/'
            else:
                back_dic['code'] = 1001
                back_dic['msg'] = "删除失败"

            return JsonResponse(back_dic)


def runinstall(request):
    if request.method == "POST":
        if request.is_ajax():
            backend_ls = []
            back_dic = {}
            back_dic['url'] = '/app/list/'
            hostpk_ls = request.POST.get("hostpk_ls")
            if not hostpk_ls:
                back_dic["code"] = 1002
                back_dic["msg"] = "请先选择主机"
                return JsonResponse(back_dic)
            shellpk_ls = request.POST.get("shellpk_ls")
            if not shellpk_ls:
                back_dic["code"] = 1003
                back_dic["msg"] = "请先选择shell脚本"
                return JsonResponse(back_dic)
            if hostpk_ls:
                hostpk_ls = hostpk_ls.split(",")
            if shellpk_ls:
                shellpk_ls = shellpk_ls.split(",")

            queryset = models.Hosts.objects.filter(id__in=hostpk_ls)
            hostdic_ls = []
            for q in queryset:
                hostdic_ls.append(model_to_dict(q))

            queryset = models.Shells.objects.filter(id__in=shellpk_ls)
            shellname_ls = []
            for q in queryset:
                shellpath = model_to_dict(q).get("path")
                if shellpath:
                    shellname = os.path.basename(str(shellpath))
                    shellname_ls.append(shellname)

        for hostdic in hostdic_ls:
            resultmsg = hostdic["host"]+"\n"
            std_out_ls = paramiko_uploadfile_to_linux(hostdic, shellname_ls)
            for std_out in std_out_ls:
                resultmsg +=std_out+ "\n"
        backend_ls.append(resultmsg)
        back_dic["code"] = 1000
        back_dic["backend_ls"] = backend_ls
        return JsonResponse(back_dic)


def upfile(request):
    if request.method == "POST":
        if request.is_ajax():
            back_dic = {}
            formobj = Shellform(request.POST)
            if formobj.is_valid():
                back_dic = {"code": 1000, 'msg': "上传文件成功"}
                clean_data = formobj.cleaned_data
                file_obj = request.FILES.get("upfile")
                if file_obj:
                    clean_data["path"] = file_obj
                    models.Shells.objects.create(**clean_data)
                    back_dic['url'] = '/app/list/'

            else:
                back_dic['code'] = 1001
                back_dic['msg'] = formobj.errors
            return JsonResponse(back_dic)
    return render(request, 'list.html', locals())


# 上传文件
def upfile(request):
    if request.method == "POST":
        if request.is_ajax():
            backend_ls = []
            back_dic = {}
            back_dic['url'] = '/app/list/'
            hostpk_ls = request.POST.get("hostpk_ls")
            if not hostpk_ls:
                back_dic = {"code": 1002, 'msg': "请先选择主机"}
                return JsonResponse(back_dic)
            linuxpath = request.POST.get("linuxpath")
            if not linuxpath:
                linuxpath = "/home"
            file = request.FILES.get("upfile")
            if not file:
                back_dic["code"] = 1003
                back_dic["msg"] = "请选择文件上传"
                return JsonResponse(back_dic)
            filename = file.name
            filepath = os.path.join('upfile',file.name)
            with open(filepath,"wb+") as wf:
                for chunk in file.chunks():
                    wf.write(chunk)

            if not linuxpath:
                linuxpath = "/home"
            if hostpk_ls:
                hostpk_ls = hostpk_ls.split(",")

            queryset = models.Hosts.objects.filter(id__in=hostpk_ls)
            hostdic_ls = []
            for q in queryset:
                hostdic_ls.append(model_to_dict(q))


            for hostdic in hostdic_ls:
                resultmsg = hostdic["host"]
                std_out = upfile_to_linux(hostdic, filename,linuxpath)
                resultmsg+=str(std_out)+"\n"
                backend_ls.append(resultmsg)
            back_dic["backend_ls"] = backend_ls
            back_dic["msg"] = backend_ls
            back_dic["code"] = 1000
            return JsonResponse(back_dic)

