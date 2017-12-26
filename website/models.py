from django.db import models
from faker import Factory
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """用户资料类"""
    belong_to = models.OneToOneField(to=User, related_name='profile')
    profile_image = models.FileField(upload_to='profile_image')


class Video(models.Model):
    """Video表字段"""
    title = models.CharField(null=True, blank=True, max_length=300)  # 文章标题
    content = models.TextField(null=True)  # 视频解说内容
    url_image = models.URLField(null=True, blank=True)  # 封面 网上的图片

    cover = models.FileField(upload_to='cover_image', null=True)  #上传图片字段

    editors_choice = models.BooleanField(default=False)  # 文章分类用的

    def __str__(self):
        return self.title



# f = open('/Users/Administrator/Desktop/111.txt', 'r')
# fake = Factory.create()
#
# for url in f.readlines():
#     v = Video(
#         title=fake.text(max_nb_chars=90),
#         content=fake.text(max_nb_chars=3000),
#         url_image=url,
#         editors_choice=fake.pybool(),
#         )
#     v.save()
