from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from . import models

# Create your views here.
import hashlib


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
            if _hash_password(password) == user.hash_password:
            # if user.password == password:
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
        print(username, password, email)
        # if not (username.strip() and password.strip() and email.strip()):
        #     print("某个字段为空")
        #     return render(request, '/register', context={'message': '某个字段为空'})
        # if len(username)>20 or len(password) >20:
        #     print("用户名和密码过长")
        # redirect('/login/')

        # 写数据库
        user = models.User.objects.filter(email=email).first()
        if user:
            '用户已存在'
            return render(request, 'register.html', context= {'message': '用户已注册'})
        hash_password = _hash_password(password)
        try:
            user1 = models.User(name=username, password=password, email=email, hash_password=hash_password)
            user1.save()
            print('保存成功')
            return redirect('/login/')
        except Exception as e:
            print(f'保存失败{e}')
            return redirect('/register/')


def logout(request):
    """登出"""
    # 清除session登出
    request.session.flush()   # 清除此用户session对应的所有sessiondata
    return redirect('/index/')


def _hash_password(password):
    """哈希加密用户注册密码"""
    sha = hashlib.sha256()
    sha.update(password.encode(encoding='utf-8'))
    return sha.hexdigest()

"""
def _hash_password(password):
    哈希加密用户注册密码 加盐版
    salt = ''
    for i in range(4)
        salt +=str(random)
    sha = hashlib.sha256()
    sha.update(password.encode(encoding='utf-8'))
    return sha.hexdigest()
 """


  # 查询数据库         # 相当于 'select * from login_user where name=%s and password=%s' %s(username, password)
        # result = models.User.objects.filter(name=username, password=password).first()


