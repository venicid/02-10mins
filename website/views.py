from django.shortcuts import render, Http404,redirect,HttpResponse
from  website.models import  Video
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from website.form import LoginForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# Create your views here.

def index_register(request):
    """注册"""
    context = {}
    if request.method == 'GET':
        form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()   #表单验证没有问题(用户名占用，不合法字符),就保存
            return redirect(to='login')
    context['form'] = form
    return render(request, 'register_login.html', context)

# 方法1：Django自带的AuthenticationForm登录表单,会帮助我们验证
def index_login(request):
    context = {}
    if request.method == 'GET':
        form = AuthenticationForm

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)        #验证
        if form.is_valid():                #用户存在，登录
            login(request, form.get_user())
            return redirect(to='list')

    context['form'] = form
    return render(request, 'register_login.html', context)

# 方法2：form表单
# def index_login(request):
#     context = {}
#     if request.method == 'GET':
#         form = LoginForm
#         print('11111111')
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         print(form)
#         if form.is_valid():
#             username = form.cleaned_data['username']   #取出数据
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)  #authenticate函数
#
#             #验证用户对象  如果是真，就True
#             if user:
#                 login(request, user)
#                 return redirect(to='list')
#             else:
#                 return HttpResponse('<h1>Not this User</h1>')
#
#     context['form'] = form
#     return render(request, 'register_login.html', context)



def listing(request, cate=None):  #cate可选默认参数
    context = {}

    if cate is None:
        video_list = Video.objects.all()
    if cate == 'editors':
        video_list = Video.objects.filter(editors_choice=True)
    else:
        video_list = Video.objects.all()

    page_rebot = Paginator(video_list, 9)  # 每页9个数据
    page_num = request.GET.get('page')

    try:
        video_list = page_rebot.page(page_num)  # get方法取哪一页
    except EmptyPage:
        video_list = page_rebot.page(page_rebot.num_pages)  # 999加载最后一页
        #raise Http404('EmptyPage')  #返回404错误
    except PageNotAnInteger:
        video_list = page_rebot.page(1)        # 432jds 加载第一页

    context['video_list'] = video_list
    listing_page = render(request, 'listing.html', context)
    return listing_page
