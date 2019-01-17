from django.shortcuts import render, redirect
from . import models

# Create your views here.


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method =='GET':
        # 用户初次进入展示登录表单
        return render(request, 'login.html')
    elif request.method == 'POST':
        content = {
            'message': '',
        }
        # 用户提交表单
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        user = models.User.objects.filter(name=username).first()
        if user:
            if user.password == password:
                content['message'] = '登录成功'
                # 服务器设置sessionid和其他用户信息。sessionid(服务器给访问他的浏览器的身份证)自动生成的
                request.session['is_login'] = True
                request.session['username'] = username
                request.session['userid'] = user.id
                return redirect('/index/')      # 返回的响应中包含set-cookie（sessionid='asda'）
            else:
                content['message'] = '密码错误'
                return render(request, 'login.html', context=content)
        else:
            content['message'] = '该用户未注册'
            return render(request, 'login.html', context=content)


def register(request):
    if request.method == 'GET':
        # 注册表表单
        return render(request, 'register.html')
    elif request.method == 'POST':
        # 后端表单验证
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if not (username.strip() and password.strip() and email.strip()):
            print("某个字段为空")
            return render(request,'/register', context={'message': '某个字段为空'})
        if len(username)>20 or  len(password) >20:
            print("用户名和密码过长")

        # 写数据库
        redirect('/login/')


def logout(request):
    """登出"""
    # 清除session登出
    request.session.flush()   # 清除此用户session对应的所有sessiondata
    return redirect('/index/')




  # 查询数据库         # 相当于 'select * from login_user where name=%s and password=%s' %s(username, password)
        # result = models.User.objects.filter(name=username, password=password).first()


