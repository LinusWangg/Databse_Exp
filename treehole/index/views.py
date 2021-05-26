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
    data['content'] = [{'head':'学校热点','url':'#'},
                    {'head':'校内论坛','url':'#'},
                    {'head':'圈地自萌','url':'#'},
                    {'head':'许愿墙','url':'#'},
                    {'head':'报个BUG','url':'#'}
                    ]
    return render(request,'index.html',data)