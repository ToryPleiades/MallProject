from django.shortcuts import render, redirect, reverse
from common.models import Users
from datetime import datetime
from common import base64

# Create your views here.


def index(request):
    """商品首页"""
    return render(request, 'web/index.html')


def lists(request, pindex=1):
    """商品列表页"""
    return render(request, 'web/list.html')


def detail(request, gid):
    """商品详情页"""
    return render(request, 'web/detail.html')


def sign_in(request):
    """用户登录"""
    return render(request, 'web/login.html')


def login(request):
    """执行登录"""
    try:
        user = Users.objects.get(username=request.POST['username'])

        # 判断当前用户状态是否正常
        if user.state == 0 or user.state == 1:
            # 验证密码
            pwd = request.POST['password']
            pwd = base64.base64_encode(pwd)
            if user.password == pwd:
                # 此处登录成功，将当前登录信息放入到session中，并跳转页面
                request.session['user'] = user.toDict()
                return redirect(reverse('web_index'))
            else:
                context = {'info': '登录密码错误！'}
        else:
            context = {'info': '此用户为非法用户！'}

    except Exception as err:
        print(err)
        context = {'info': '登录账号错误！'}
    return render(request, 'web/login.html', context)


def sign_out(request):
    """用户登出"""
    # 清除登录的session信息
    del request.session['user']
    # 跳转登录页面
    return redirect(reverse('web_sign_in'))


def register(request):
    """注册会员"""
    return render(request, 'web/register.html')


def regist(request):
    """执行注册"""
    try:
        ob = Users()  # 实例化Users模型
        ob.username = request.POST['registerUsername']

        # 密码base64加密
        pwd = request.POST['registerPassword']
        pwd = base64.base64_encode(pwd)
        ob.password = pwd
        ob.sex = 1
        ob.state = 1
        ob.addtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ob.save()  # 将数据存储至数据库

        user = Users.objects.get(username=request.POST['registerUsername'])
        request.session['user'] = user.toDict()

        return redirect(reverse('web_index'))
    except Exception as err:
        print(err)
        return redirect(reverse('web_sign_in'))
