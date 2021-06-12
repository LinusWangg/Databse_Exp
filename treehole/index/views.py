from django.shortcuts import render
import requests
# Create your views here.

def primary_data(request):
    data = {}
    if(request.session.get('is_login',None)):
        data['user_name'] = request.session['user_name']
    else:
        data['user_name'] = 'wywnb'
    data['title'] = '南航树洞'
    data['content'] = [{'head':'文章搜索','url':'http://127.0.0.1:8000/article'},
                    {'head':'文章编写','url':'http://127.0.0.1:8000/article/write'},
                    {'head':'我的主页','url':'http://127.0.0.1:8000/article/getauthorart'},
                    {'head':'许愿墙','url':'#'},
                    {'head':'报个BUG','url':'#'}
                    ]
    return render(request,'index.html',data)