from django.shortcuts import render, Http404,redirect,HttpResponse
from  website.models import  Video,Ticket
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login
from website.form import LoginForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
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


def detail(request, id):
    """投票的id,视频的ID """
    context = {}
    vid_info = Video.objects.get(id=id)  #投票的是哪个视频
    voter_id = request.user.profile.id  # 投票的是哪个用户

    #视频id 里面有多少like  count（like）
    like_counts = Ticket.objects.filter(choice='like', video_id=id).count()

    try:
        user_ticker_for_this_video = Ticket.objects.get(voter_id=voter_id, video_id=id)
        # 这个视频，这个用户，投票的内容是什么
        context['user_ticket'] = user_ticker_for_this_video
        print(context['user_ticket'].choice)
    except:
        pass

    context['vid_info'] = vid_info
    context['like_counts'] = like_counts
    return render(request, 'detail.html', context)


def detail_vote(request, id):
    voter_id = request.user.profile.id
    try:   #如果已经投票了，显示之前的
        user_ticket_for_this_video = Ticket.objects.get(voter_id=voter_id, video_id=id)
        user_ticket_for_this_video.choice = request.POST['vote']
        user_ticket_for_this_video.save()
    except ObjectDoesNotExist:  # 如果没有投票，就投票
        new_ticket = Ticket(voter_id=voter_id, video_id=id, choice=request.POST['vote'])
        print(new_ticket)
        new_ticket.save()

    return redirect(to='detail', id=id)
