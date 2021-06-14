#from django.db.models.fields import PositiveBigIntegerField
from django.shortcuts import redirect, render
from django.db import connection
from django.core import serializers
from django.http import HttpResponse,JsonResponse,FileResponse, response
from django.views import View
from utils.response import wrap_json_response,ReturnCode,CommonResponseMixin
import json
import requests
from .models import Article,Comment
from user.views import findUserbyname
from hashlib import md5
import os
import treehole.settings as settings
import datetime
from user import views as usr_view
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
                    {'head':'个人信息','url':'http://127.0.0.1:8000'},
                    {'head':'报个BUG','url':'#'}
                    ]
    data['type'] = [{'type':'动画','url':'http://127.0.0.1:8000/article/blog/#','index':'2'},
                    {'type':'游戏','url':'http://127.0.0.1:8000/article/blog/#','index':'1'},
                    {'type':'生活','url':'http://127.0.0.1:8000/article/blog/#','index':'28'},
                    {'type':'影视','url':'http://127.0.0.1:8000/article/blog/#','index':'3'},
                    {'type':'科技','url':'http://127.0.0.1:8000/article/blog/#','index':'17'},
                    {'type':'笔记','url':'http://127.0.0.1:8000/article/blog/#','index':'41'},
                    {'type':'小说','url':'http://127.0.0.1:8000/article/blog/#','index':'16'},]
    return render(request,'blog_all.html',data)

def primary_data2(request):
    data = {}
    if(request.session.get('is_login',None)):
        data['user_name'] = request.session['user_name']
    else:
        data['user_name'] = 'wywnb'
    data['title'] = '南航树洞'
    data['content'] = [{'head':'文章搜索','url':'http://127.0.0.1:8000/article'},
                    {'head':'文章编写','url':'http://127.0.0.1:8000/article/write'},
                    {'head':'我的主页','url':'http://127.0.0.1:8000/article/getauthorart'},
                    {'head':'个人信息','url':'http://127.0.0.1:8000'},
                    {'head':'报个BUG','url':'#'}
                    ]
    data['type'] = [{'type':'动画','url':'http://127.0.0.1:8000/article/blog/#','index':'2'},
                    {'type':'游戏','url':'http://127.0.0.1:8000/article/blog/#','index':'1'},
                    {'type':'生活','url':'http://127.0.0.1:8000/article/blog/#','index':'28'},
                    {'type':'影视','url':'http://127.0.0.1:8000/article/blog/#','index':'3'},
                    {'type':'科技','url':'http://127.0.0.1:8000/article/blog/#','index':'17'},
                    {'type':'笔记','url':'http://127.0.0.1:8000/article/blog/#','index':'41'},
                    {'type':'小说','url':'http://127.0.0.1:8000/article/blog/#','index':'16'},]
    return render(request,'blog.html',data)

def primary_data3(request):
    data = {}
    if(request.session.get('is_login',None)):
        data['user_name'] = request.session['user_name']
    else:
        data['user_name'] = 'wywnb'
    data['title'] = '南航树洞'
    data['content'] = [{'head':'文章搜索','url':'http://127.0.0.1:8000/article'},
                    {'head':'文章编写','url':'http://127.0.0.1:8000/article/write'},
                    {'head':'我的主页','url':'http://127.0.0.1:8000/article/getauthorart'},
                    {'head':'个人信息','url':'http://127.0.0.1:8000'},
                    {'head':'报个BUG','url':'#'}
                    ]
    return render(request,'write_blog.html',data)

def primary_data4(request):
    data = {}
    if(request.session.get('is_login',None)):
        data['user_name'] = request.session['user_name']
    else:
        data['user_name'] = 'wywnb'
    data['title'] = '南航树洞'
    data['content'] = [{'head':'文章搜索','url':'http://127.0.0.1:8000/article'},
                    {'head':'文章编写','url':'http://127.0.0.1:8000/article/write'},
                    {'head':'我的主页','url':'http://127.0.0.1:8000/article/getauthorart'},
                    {'head':'个人信息','url':'http://127.0.0.1:8000'},
                    {'head':'报个BUG','url':'#'}
                    ]
    return render(request,'myart.html',data)

def findbyarttitle(art_title):
    Art = Article.objects.raw("select * from article_article where art_title = %s",[art_title])
    if not Art:
        return None
    Art = serializers.serialize("json",Art)
    Art = json.loads(Art)[0]
    Art['fields']['art_title'] = Art['pk']
    return Art['fields']

def findbyauthor(art_author):
    Art = Article.objects.raw("select art_title,art_author,art_time,art_type,art_pic from article_article where art_author = %s",[art_author])
    Articles = []
    for x in Art:
        Articles.append(x)
    return Articles

def deletemine(art_title,user_name,user_pwd):
    user = findUserbyname(user_name)
    if(user.user_pwd != user_pwd):
        return False
    else:
        Article.objects.raw("delete from article_article where art_title = %s",[art_title])
        return True

def writearticle(request):
    data = {}
    user_name = request.POST.get("art_author")
    art_title = request.POST.get("art_title")
    if(findbyarttitle(art_title)):
        data['Exist'] = True
    else:
        data['Exist'] = False
        art_content = request.POST.get('art_content')
        art_type = request.POST.get('art_type')
        user_avatar = request.FILES.get('file')
        file_name = str(art_title)+'.jpg'
        file_path = os.path.join(settings.BASE_DIR,'media/art_pic',file_name)
        with open(file_path, 'wb') as f:
            for chunk in user_avatar.chunks():
                f.write(chunk)
        artpicpath = "http://localhost:8000/media/art_pic/"+str(art_title)+".jpg"
        art_author = user_name
        art_time = datetime.datetime.now()
        article = Article(art_title=art_title,art_time=art_time,art_content=art_content,art_author=art_author,art_type=art_type,art_pic=artpicpath)
        article.save()
    response = wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success!')
    return JsonResponse(data=response,safe=False)

def deletemyart(request):
    data = {}
    post_data = request.body.decode("utf-8")
    post_data = json.loads(post_data)
    art_title = post_data.get("art_title")
    user_name = post_data.get('user_name')
    user_pwd = post_data.get('user_pwd')
    user_pwd = md5(user_pwd.encode('utf8')).hexdigest()
    data['Allow'] = deletemine(art_title,user_name,user_pwd)
    response = wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success!')
    return JsonResponse(data=response,safe=False)

def writecomment(request):
    data = {}
    post_data = request.body.decode("utf-8")
    post_data = json.loads(post_data)
    art_title = post_data.get('art_title')
    commentor = post_data.get('user_name')
    commentwho = post_data.get('comment_id')
    comment_content = post_data.get('comment_content')
    comment_time = datetime.datetime.now()
    sql = "insert into article_comment(art_title,commentor,commentwho,comment_content,comment_time) values('{0}','{1}',{2},'{3}','{4}');".format(
        art_title,commentor,commentwho,comment_content,comment_time
    )
    cur = connection.cursor()
    data['success'] = cur.execute(sql)
    data['success'] = True
    cur.close()
    response = wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success!')
    return JsonResponse(data=response,safe=False)

def search(request):
    data = {}
    post_data = request.body.decode("utf-8")
    post_data = json.loads(post_data)
    key_word = post_data.get('key_word')
    if(key_word):
        key_word = '%'+str(post_data.get('key_word'))+'%'
    else:
        key_word = '%'
    time_from = post_data.get('time_from')
    time_to = post_data.get('time_to')
    art_type = post_data.get('type')
    if art_type == "99":
        art_type = '%'
    page = post_data.get('page')
    Arts = []
    page_from = 10*(page-1)
    page_to = 10*page
    # 分页
    arts = Article.objects.raw("select art_title,art_author,art_time,art_type,art_pic from article_article where art_title like %s and art_time between %s and %s and art_type like %s limit %s,%s",[key_word,time_from,time_to,art_type,page_from,page_to])
    arts = serializers.serialize("json",arts)
    arts = json.loads(arts)
    for x in arts:
        x['fields']['art_title'] = x['pk']
        Arts.append(x['fields'])

    data['Arts'] = Arts
    response = wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success!')
    return JsonResponse(data=response,safe=False)

def getmine(request):
    data = {}
    post_data = request.body.decode("utf-8")
    post_data = json.loads(post_data)
    art_author = post_data.get('user_name')
    page = post_data.get('page')
    Arts = []
    i = 0
    page_from = 10*(page-1)
    page_to = 10*page
    # 分页
    arts = Article.objects.raw("select art_title,art_author,art_time,art_type,art_pic from article_article where art_author = %s limit %s,%s",[art_author,page_from,page_to])
    arts = serializers.serialize("json",arts)
    arts = json.loads(arts)
    for x in arts:
        x['fields']['art_title'] = x['pk']
        Arts.append(x['fields'])

    data['Arts'] = Arts
    response = wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success!')
    return JsonResponse(data=response,safe=False)

# admin module
def getall(request):
    data = {}
    post_data = request.body.decode("utf-8")
    post_data = json.loads(post_data)
    page = post_data.get('page')
    Arts = []
    page_from = 10*(page-1)
    page_to = 10*page
    # 分页
    arts = Article.objects.raw("select art_title,art_author,art_time,art_type,art_pic from article_article limit %s,%s",[page_from,page_to])
    arts = serializers.serialize("json",arts)
    arts = json.loads(arts)
    for x in arts:
        x['fields']['art_title'] = x['pk']
        Arts.append(x['fields'])

    data['Arts'] = Arts
    response = wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success!')
    return JsonResponse(data=response,safe=False)

def dictfetchall(cursor):
    "将游标返回的结果保存到一个字典对象中"
    desc = cursor.description
    return [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]

def getsum(request):
    data = {}
    post_data = request.body.decode("utf-8")
    post_data = json.loads(post_data)
    page = post_data.get('page')
    Art_info_author = []
    page_from = 10*(page-1)
    page_to = 10*page
    cur = connection.cursor()
    cur.execute("select art_author,count(*) from article_article group by art_author limit %s,%s",[page_from,page_to])
    Art_info_author = dictfetchall(cur)
    cur.close()
    
    data['Arts'] = Art_info_author
    response = wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success!')
    return JsonResponse(data=response,safe=False)

def getdate(request):
    data = {}
    post_data = request.body.decode("utf-8")
    post_data = json.loads(post_data)
    page = post_data.get('page')
    Art_time = []
    page_from = 10*(page-1)
    page_to = 10*page
    time_from = post_data.get('time_from')
    time_to = post_data.get('time_to')
    arts = Article.objects.raw("select art_title,art_author,art_time,art_type,art_pic from article_article where art_time between %s and %s limit %s,%s",[time_from,time_to,page_from,page_to])
    arts = serializers.serialize("json",arts)
    arts = json.loads(arts)
    for x in arts:
        x['fields']['art_title'] = x['pk']
        Art_time.append(x['fields'])
    data['Arts'] = Art_time
    response = wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success!')
    return JsonResponse(data=response,safe=False)
    
def getdetail(request):
    data = {}
    post_data = request.body.decode("utf-8")
    post_data = json.loads(post_data)
    art_title = post_data.get('art_title')
    Article = findbyarttitle(art_title)
    data['Arts'] = Article
    user = usr_view.findUserbyname(Article['art_author'])[0]
    data['author_avatar'] = user.user_avatar
    response = wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success!')
    return JsonResponse(data=response,safe=False)

def timedata(request):
    data = []
    post_data = request.body.decode("utf-8")
    post_data = json.loads(post_data)
    user_name = post_data.get('user_name')
    cur = connection.cursor()
    cur.execute("select art_time,count(*) from (select * from article_article where art_author = '"+user_name+"') GROUP BY art_time")
    temp = dictfetchall(cur)
    for x in temp:
        data.append([x['art_time'],x['count']])
    cur.close()
    response = wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success!')
    return JsonResponse(data=response,safe=False)

def getcomment(request):
    data = {}
    wcnm = {}
    cur = connection.cursor()
    post_data = request.body.decode("utf-8")
    post_data = json.loads(post_data)
    art_title = post_data.get('art_title')
    comment = Comment.objects.raw("select * from article_comment where art_title = '{0}' order by commentwho".format(art_title))
    comment = serializers.serialize("json",comment)
    comment = json.loads(comment)
    comment_temp = []
    for x in comment:
        x['fields']['comment_id'] = x['pk']
        comment_temp.append(x['fields'])
    comments = {}
    for x in comment_temp:
        if(x['commentwho']==0):
            cur.execute("select user_avatar from user_user where user_name = '{0}'".format(x['commentor']))
            comments[x['comment_id']] = {}
            wcnm = dictfetchall(cur)
            if len(wcnm)>0:
                comments[x['comment_id']]['commentor_avatar'] = wcnm[0]['user_avatar']
            comments[x['comment_id']]['commentor'] = x['commentor']
            comments[x['comment_id']]['comment_content'] = x['comment_content']
            comments[x['comment_id']]['comment_time'] = x['comment_time']
            comments[x['comment_id']]['comment_list'] = {}
            comments[x['comment_id']]['comment_id'] = x['comment_id']
        else:
            temp_s = []
            temp_comments = comments
            temp = Comment.objects.raw("select * from article_comment where comment_id = %s",[x['commentwho']])
            while temp:
                temp = serializers.serialize("json",temp)
                temp = json.loads(temp)
                temp[0]['fields']['comment_id'] = temp[0]['pk']
                temp = temp[0]['fields']
                temp_s.append(temp['comment_id'])
                temp = Comment.objects.raw("select * from article_comment where comment_id = %s",[temp['commentwho']])
            while len(temp_s)>0:
                temp_comments = temp_comments[temp_s.pop()]['comment_list']
            cur.execute("select user_avatar from user_user where user_name = '{0}'".format(x['commentor']))
            temp_comments[x['comment_id']] = {}
            wcnm = dictfetchall(cur)
            if len(wcnm)>0:
                temp_comments[x['comment_id']]['commentor_avatar'] = wcnm[0]['user_avatar']
            temp_comments[x['comment_id']]['commentor'] = x['commentor']
            temp_comments[x['comment_id']]['comment_content'] = x['comment_content']
            temp_comments[x['comment_id']]['comment_time'] = x['comment_time']
            temp_comments[x['comment_id']]['comment_list'] = {}
            temp_comments[x['comment_id']]['comment_id'] = x['comment_id']
    
    cur.close()
    data['comments'] = comments
    response = wrap_json_response(data=data,code=ReturnCode.SUCCESS,message='Success!')
    return JsonResponse(data=response,safe=False)