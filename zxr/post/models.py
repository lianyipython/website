from django.contrib.auth.models import User
from django.db import models
from tinymce import models as tinymce_models
from category.models import Category
import re


# 美食分享文章
class Post(models.Model):
    title = models.CharField('标题', max_length=100)
    cover = models.ImageField('封面', upload_to='images/%Y/%m/%d/', null=True)
    content = tinymce_models.HTMLField('文章内容')
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name='发布者')
    create_date = models.DateTimeField('创建时间', auto_now_add=True)
    modify_date = models.DateTimeField('修改时间', auto_now_add=True)
    order = models.IntegerField('排序', default=0)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE, verbose_name='分类')
    is_delete = models.BooleanField('标记为删除', default=False)
    pv = models.IntegerField('浏览量', default=1)
    check = models.BooleanField('审核通过', default=False)
    go_index = models.BooleanField('推荐到首页', default=False)

    class Meta:
        verbose_name_plural = '文章'
        ordering = ['-id']

    def __str__(self):
        return self.title

    # 文章的保存
    def post_save(self, request):
        # 获取表单数据
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        category_id = int(request.POST.get('category_id', 0))
        cover = request.FILES.get('cover')

        # 保存信息
        self.title = title
        self.content = content
        self.author = request.user
        self.category_id = category_id
        self.cover = cover

        # 保存到数据库
        self.save()

        return self

    # 文章的编辑
    def post_edit(self, request):
        # 获取表单数据
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        category_id = int(request.POST.get('category_id', 0))
        cover = request.FILES.get('cover')

        # 保存信息
        self.title = title
        self.content = content
        self.author = request.user
        self.category_id = category_id

        # 如果有新的封面
        if cover:
            self.cover = cover

        # 保存到数据库
        self.save()

        return self

    # 去除html标签，用于简洁文章内容
    def no_html_content(self):
        html = self.content
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', html)
        return dd

    # 获取我的评论数
    def post_comment_count(self):
        return self.comment_set.all().count()


# 美食分享的评论
class Comment(models.Model):
    content = tinymce_models.HTMLField('帖子评论')
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, verbose_name='回帖者')
    create_date = models.DateTimeField('回帖时间', auto_now_add=True)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    is_delete = models.BooleanField('标记为删除', default=False)

    class Meta:
        verbose_name_plural = '评论'
        ordering = ['-id']

    def __str__(self):
        return self.content

    # 去除html标签，用于简洁文章内容
    def no_html_content(self):
        html = self.content
        dr = re.compile(r'<[^>]+>', re.S)
        dd = dr.sub('', html)
        return dd


# 编辑文章需要保存的图片
class Post_images(models.Model):
    image = models.ImageField('封面', upload_to='images/%Y/%m/%d/', null=True)

    def get_url(self):
        return self.image.url
