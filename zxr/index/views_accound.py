from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

# 注册页面
from category.models import Category
from post.models import Post


def register_page(request):
    return render(request, 'index/account/register.html', {

    })


# 注册
def register_save(request):
    # 获取基本信息，为了安全起见
    # 服务器端对用户关键信息也进行验证
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    # 检测数据是否填写
    if username and password:
        if not User.objects.filter(username=username).exists():
            # 创建user
            # 该用户还未注册
            user = User()
            user.username = username
            user.set_password(password)
            user.is_staff = False
            user.is_superuser = False
            user.save()

            # 马上登录
            login(request, user)

            # 导航主页
            return redirect(reverse('index:register_success') + '?msg_info=' + "恭喜您注册成功！")
        else:
            # 该用户已注册
            return render(request, 'index/account/register.html', {
                'error_msg': "该用户名已被注册！"
            })
    else:
        # 有空值说明服务器验证有问题
        # 返回登录页面说明问题
        return redirect(reverse('gd168_pc:account_registing'))


# 登录页面
def login_page(request):
    error_msg = request.GET.get('error_msg', '')
    return render(request, 'index/account/login.html', {
        'error_msg': error_msg
    })


# 登录操作
def user_login(request):
    # 用户登录的逻辑
    username = request.POST.get('username', False)
    password = request.POST.get('password', False)
    if username and password:
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse('index:register_success') + '?msg_info=' + "欢迎回来！！")
            else:
                return redirect(reverse('index:login_page') + '?error_msg=%s' % '你的账号已被封！')
        else:
            return redirect(reverse('index:login_page') + '?error_msg=%s' % '用户名或密码错误！')
    else:
        return redirect(reverse('index:login_page') + '?error_msg=%s' % '用户名和密码不能为空！')


# 用户登出
def user_logout(request):
    logout(request)
    return redirect(reverse('index:index'))


# register 成功
def register_success(request):
    # 文章的分类
    categories = Category.objects.filter(is_delete=False)
    msg_info = request.GET.get('msg_info', '')
    return render(request, 'index/success/accound_success.html', {
        'msg_info': msg_info,
        'categories':categories
    })


# 我的文章列表
def my_post_list(request, page=1):

    categories = Category.objects.filter(is_delete=False)

    # 文章的分类
    post_list = Post.objects.filter(is_delete=False, author=request.user)
    paginator = Paginator(post_list, 10)
    page_num = int(page)

    if page_num < 1:
        current_page = 1
    elif page_num > paginator.num_pages:
        current_page = paginator.num_pages
    else:
        current_page = page_num

    posts = paginator.page(current_page)
    return render(request, 'index/account/my_post_list.html', {
        'categories':categories,
        'posts': posts,
        'page_num': current_page,
        'page_num_previous': current_page - 1,
        'page_num_next': current_page + 1,
        'page': int(page),
        'page_range': paginator.page_range
    })


# 编辑文章
def edit_my_post(request, post_id=0):
    categories = Category.objects.filter(is_delete=False)
    post = Post.objects.get(is_delete=False, pk=post_id)
    return render(request, 'index/post_publish.html', {
        'post': post,
        'categories':categories
    })

