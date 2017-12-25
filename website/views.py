from django.shortcuts import render, Http404
from  website.models import  Video
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


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
