from io import BytesIO


from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import HttpResponseRedirect

# Create your views here.
from . import models
from . import utils


def users_register(request):
    if request.method == "GET":
        return render(request, "users/register.html/", {"msg": "请认真填写如下信息！"})
    elif request.method == "POST":
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()
        confirmpwd = request.POST["confirmpwd"].strip()
        nickname = request.POST["nickname"].strip()
        code = request.POST["code"].strip()
        # 多张照片时候，循环保存
        # avatar = request.FILES.getlist("avatar")

        # 数据校验
        if username == "":
            return render(request, "users/register.html", {"msg": "用户名称不能为空"})
        if len(password) < 6:
            return render(request, "users/register.html", {"msg": "用户密码长度不能少于6位！"})
        if password.strip() != confirmpwd.strip():
            return render(request, "users/register.html", {"msg": "两次密码不一致！"})
        if nickname == "":
            return render(request, "users/register.html", {"msg": "用户昵称不能为空"})
        if code.lower() != request.session["code"].lower():
            return render(request, "users/login.html", {"msg": "验证码错误！！"})

        # 用户名称不能重复
        try:
            models.User.objects.get(username=username)
            return render(request, "users/register.html", {"msg": "该用户名称已存在，请重新输入！"})
        except:
            try:
                password = utils.md5_hashlib(password)
                user = models.User(username=username, password=password, nickname=nickname)
                user.save()
            except:
                return render(request, "users/register.html", {"msg": "注册失败，请重新注册！"})
        return render(request, "users/login.html", {"msg": "用户注册成功，请登录"})


def users_login(request):
    if request.method == "GET":
        return render(request, "users/login.html/", {"msg": "亲，欢迎您！登录吧。"})
    else:
        # 接收页面的参数。
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()
        code = request.POST["code"].strip()

        # 数据校验
        if code.lower() != request.session["code"].lower():
            return render(request, "users/login.html", {"msg": "验证码错误！！"})
        if username == "":
            return render(request, "users/login.html", {"msg": "用户名称不能为空！"})
        if password == "":
            return render(request, "users/login.html", {"msg": "用户密码不能为空！"})

        users = models.User.objects.filter(username=username)
        if len(users)>0:
            password = utils.md5_hashlib(password)
            if users[0].password == password:
                print("登录成功")
                # 保存用户的信息 以表示用户已经登录
                # 跳转用户列表界面
                # import pickle, json
                # pickle.dump()
                request.session["first_session"] = users[0]
                request.session.set_expiry(0)
                return HttpResponseRedirect("index.html")

            else:
                return render(request, "users/login.html", {"msg": "密码错误！"})
        else:
            return render(request, "users/login.html", {"msg": "用户名或密码错误！"})


def login_out(request):
    try:
        del request.session["first_session"]
        return render(request, "users/login.html", {"msg": "退出成功，请重新登录！！"})
    except:
        return render(request, "users/login.html", {"msg": "退出成功，请重新登录！！"})


def users_update(request):
    pass


def code(request):
    img, msg = utils.create_code()

    f = BytesIO()
    img.save(f, "PNG")

    # 将验证码的值存储到session
    request.session["code"] = msg

    return HttpResponse(f.getvalue(), "image/png")

