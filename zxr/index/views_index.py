from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from category.models import Category
from post.models import Post, Comment, Post_images
import json


def index(request):
    # 文章的分类
    categories = Category.objects.filter(is_delete=False)

    # 推荐到首页的文章
    posts = Post.objects.filter(is_delete=False, check=True, go_index=True)

    # 把推荐数据摆好
    try:
        post_index_0 = posts[0]
    except Exception:
        post_index_0 = None

    try:
        post_index_1 = posts[1]
    except Exception:
        post_index_1 = None

    try:
        post_index_2 = posts[2]
    except Exception:
        post_index_2 = None

    try:
        post_index_3 = posts[3]
    except Exception:
        post_index_3 = None

    try:
        post_index_4 = posts[4]
    except Exception:
        post_index_4 = None

    # 最新发布文章
    new_posts = Post.objects.filter(is_delete=False, check=True)[:10]

    # 最新评论
    new_comments = Comment.objects.filter(is_delete=False)[:10]

    return render(request, 'index/index.html', {
        'categories': categories,
        # 推荐数据
        'post_index_0': post_index_0,
        'post_index_1': post_index_1,
        'post_index_2': post_index_2,
        'post_index_3': post_index_3,
        'post_index_4': post_index_4,
        'new_posts': new_posts,
        'new_comments': new_comments
    })


# 文章列表
def post_list(request, category_id=0, page=0):
    # 文章的分类
    categories = Category.objects.filter(is_delete=False)

    # 获取到正确的文章列表
    posts = Post.objects.filter(is_delete=False, check=True)

    # 列表大分类标题
    category_title = '所有的分享影评'

    # 开始分类筛选
    if int(category_id):
        posts = posts.filter(category_id=category_id)
        category_title = Category.objects.get(pk=int(category_id)).name

    paginator = Paginator(posts, 30)
    page_num = int(page)

    if page_num < 1:
        current_page = 1
    elif page_num > paginator.num_pages:
        current_page = paginator.num_pages
    else:
        current_page = page_num

    return render(request, 'index/post_list.html', {
        'categories': categories,
        'posts': paginator.page(current_page),
        'page': int(page),
        'page_range': paginator.page_range,
        'category_id': category_id,
        'posts_count':posts.count(),
        'category_title': category_title
    })


# 发布文章
def post_publish_page(request):
    categories = Category.objects.filter(is_delete=False)
    return render(request, 'index/post_publish.html', {
        'categories': categories
    })


# 文章的保存
def post_publish(request):
    post_id = int(request.POST.get('post_id', 0))
    if not post_id:
        Post().post_save(request)
        info = "亲! 您的分享已发布成功，正在等待审核！"
        return redirect(reverse("index:post_success") + '?msg_info=' + info)
    else:
        post = Post.objects.get(pk=post_id)
        post.post_edit(request)
        info = "您的文章已完成编辑"
        return redirect(reverse("index:post_success") + '?msg_info=' + info)


# 文章编辑成功提示页面
def post_success(request):
    # 文章的分类
    categories = Category.objects.filter(is_delete=False)

    msg_info = request.GET.get('msg_info', '')
    return render(request, 'index/success/publish_success.html', {
        'msg_info': msg_info,
        'categories':categories
    })


# 查看文章内容
def post_show(request, post_id=0, comment_page=0):
    # 文章分类
    categories = Category.objects.filter(is_delete=False)

    # 获取文章信息
    post = Post.objects.get(pk=post_id)

    # 增加pv数
    post.pv += 1
    post.save()

    # 获取评论
    comment_list = Comment.objects.filter(is_delete=False, post=post)
    paginator = Paginator(comment_list, 15)
    page_num = int(comment_page)

    if page_num < 1:
        current_page = 1
    elif page_num > paginator.num_pages:
        current_page = paginator.num_pages
    else:
        current_page = page_num

    # 最新文章分享
    new_posts = Post.objects.filter(is_delete=False, check=True)[:10]

    comments = paginator.page(current_page)
    return render(request, 'index/post_show.html', {
        'categories': categories,
        'post': post,
        'comment_list': comments,
        'comment_count':comment_list.count(),
        'comment_page': int(comment_page),
        'page_range': paginator.page_range,
        'new_posts': new_posts
    })


# 回复文章内容
def post_comment(request):
    # 获取信息
    post_id = int(request.POST.get('post_id', 0))
    comment = request.POST.get('comment', '')

    # 生成评论
    Comment(
        content=comment,
        author=request.user,
        post=Post.objects.get(pk=post_id)
    ).save()
    return redirect(reverse("index:post_show", kwargs={'post_id': post_id, 'comment_page': 1}))


# 文章删除自己的评论
def delete_comment(request, comment_id=0):
    # 获取要删除的评论
    comment = Comment.objects.get(pk=comment_id)
    post_id = comment.post.id

    # 从数据库中删除这个评论
    comment.delete()
    return redirect(reverse("index:post_show", kwargs={'post_id': post_id, 'comment_page': 1}))


# 删除一篇文章
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.is_delete = True
    post.save()
    info = "这个文章已删除"
    return redirect(reverse("index:post_success") + '?msg_info=' + info)


# 编辑文章保存图片
@csrf_exempt
def image_save(request):
    # 将图片保存到专门
    image = Post_images(
        image=request.FILES['image']
    )
    image.save()

    response_data = {
        "success": True,
        "msg": "error message",
        "file_path": image.get_url()
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")
