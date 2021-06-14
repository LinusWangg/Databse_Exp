from django.shortcuts import redirect, render
from django.http import HttpResponse,JsonResponse,FileResponse
from django.views import View
from utils.response import wrap_json_response,ReturnCode,CommonResponseMixin
import json
import requests
from .models import User
from hashlib import md5
import os
import treehole.settings as settings
from django.db import connection
# Create your views here.
def primary_data1(request):
    data = {}
    data['title'] = '南航树洞'
    data['content'] = [{'head':'文章搜索','url':'http://127.0.0.1:8000/article'},
                    {'head':'文章编写','url':'http://127.0.0.1:8000/article/write'},
                    {'head':'我的主页','url':'http://127.0.0.1:8000/article/getauthorart'},
                    {'head':'个人信息','url':'http://127.0.0.1:8000'},
                    {'head':'报个BUG','url':'#'}
                    ]
    return render(request,'signin.html',data)

def primary_data2(request):
    data = {}
    data['title'] = '南航树洞'
    data['content'] = [{'head':'文章搜索','url':'http://127.0.0.1:8000/article'},
                    {'head':'文章编写','url':'http://127.0.0.1:8000/article/write'},
                    {'head':'我的主页','url':'http://127.0.0.1:8000/article/getauthorart'},
                    {'head':'个人信息','url':'http://127.0.0.1:8000'},
                    {'head':'报个BUG','url':'#'}
                    ]
    return render(request,'signup.html',data)

def logout(request):
    request.session.clear()
    return redirect('/')

def findUserbyact(user_act):
    #user = User.objects.filter(user_act=user_act).first()
    user = User.objects.raw("select * from user_user where user_act = %s",[user_act])
    return user

def findUserbyname(user_name):
    #user = User.objects.filter(user_name=user_name).first()
    user = User.objects.raw("select * from user_user where user_name = %s",[user_name])
    return user

def findUser(user_act,user_pwd):
    #user = User.objects.filter(user_act=user_act,user_pwd=user_pwd).first()
    user = User.objects.raw("select * from user_user where user_act = %s and user_pwd = %s",[user_act,user_pwd])[0]
    return user

def userinfo(request):
    data = {}
    post_data = request.body.decode("utf-8")
    post_data = json.loads(post_data)
    user_name = post_data.get('user_name')
    user = findUserbyname(user_name)[0]
    data['user_act'] = user.user_act
    data['user_name'] = user.user_name
    if(user.user_avatar):
        data['user_avatar'] = user.user_avatar
    else:
        data['user_avatar'] = "http://127.0.0.1:8000/media/avatar/2.jpg"
    data['user_birth'] = user.user_birth
    response=wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success')
    return JsonResponse(data=response,safe=False)

def signup(request):
    data = {}
    post_data = request.body.decode("utf-8")
    post_data = json.loads(post_data)
    if request.method == 'GET':
        response=wrap_json_response(code=ReturnCode.FAILED,message='NOT GET!')
        return JsonResponse(data=response,safe=False)
    else:
        user_act = post_data.get('user_act')
        user = findUserbyact(user_act)
        if user:
            data['is_register'] = True
            response=wrap_json_response(data=data,code=ReturnCode.FAILED,message='UserAccount Exist!')
            return JsonResponse(data=response,safe=False)
        else:
            user_pwd = post_data.get('user_pwd')
            user_pwd = md5(user_pwd.encode('utf8')).hexdigest()
            user_name = post_data.get('user_name')
            user_birth = post_data.get('user_birth')
            user = User(user_act=user_act,user_pwd=user_pwd,user_name=user_name,user_birth=user_birth)
            user.save()
            data['user_act'] = user_act
            data['is_register'] = False
            response = wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success!')
            return JsonResponse(data=response,safe=False)

def signin(request):
    request.session.clear()
    data = {}
    post_data = request.body.decode("utf-8")
    post_data = json.loads(post_data)
    user_act = post_data.get('user_act')
    user_pwd = post_data.get('user_pwd')
    user_pwd = md5(user_pwd.encode('utf8')).hexdigest()
    user = findUser(user_act,user_pwd)
    if user:
        data['login_succeed'] = True
        data['user_name'] = user.user_name
        request.session['user_name'] = user.user_name
        request.session['is_login'] = True
        response=wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success!')
        return JsonResponse(data=response,safe=False)
    else:
        data['login_succeed'] = False
        response=wrap_json_response(data=data,code=ReturnCode.FAILED,message='Denied!')
        return JsonResponse(data=response,safe=False)

def modify_name(request):
    data = {}
    post_data = request.body.decode("utf-8")
    post_data = json.loads(post_data)
    user_act = post_data.get('user_act')
    user_name = post_data.get('user_name')
    user = findUserbyact(user_act)
    if user:
        user.update(user_name = user_name)
        response = wrap_json_response(code=ReturnCode.SUCCESS,message='Success!')
        return JsonResponse(data=response,safe=False)
    else:
        response=wrap_json_response(code=ReturnCode.FAILED,message='No user!')
        return JsonResponse(data=response,safe=False)

def modify_avatar(request):
    data = {}
    user_act = request.POST.get('user_act')
    user_avatar = request.FILES.get('file')
    file_name = str(user_act)+'.jpg'
    file_path = os.path.join(settings.BASE_DIR,'media/avatar',file_name)
    with open(file_path, 'wb') as f:
        for chunk in user_avatar.chunks():
            f.write(chunk)

    user = findUserbyact(user_act)
    if user:
        user_avatar = "http://localhost:8000/media/avatar/"+str(user_act)+".jpg"
        print(user_avatar,user_act)
        cur = connection.cursor()
        cur.execute("update user_user set user_avatar = %s where user_act = %s",[user_avatar,user_act])
        cur.close()
        data['user_act'] = user_act
        data['user_avatar'] = user_avatar
        data['success'] = True
        response = wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success!')
        return JsonResponse(data=response,safe=False)
    else:
        data['success'] = False
        response=wrap_json_response(code=ReturnCode.FAILED,message='No user!')
        return JsonResponse(data=response,safe=False)
        