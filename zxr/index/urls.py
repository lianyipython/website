from django.conf.urls import url
from index import views_accound,views_index

urlpatterns = [
    # 首页及其他
    url(r'^$', views_index.index, name='index'),

    # 账户
    url(r'^accound/register/page$', views_accound.register_page, name='register_page'),
    url(r'^accound/register/save$', views_accound.register_save, name='register_save'),
    url(r'^accound/login/page$', views_accound.login_page, name='login_page'),
    url(r'^accound/login$', views_accound.user_login, name='login'),
    url(r'^accound/logout$', views_accound.user_logout, name='logout'),
    url(r'^accound/success$', views_accound.register_success, name='register_success'),
    url(r'^accound/my/post/list/(?P<page>\d+)$', views_accound.my_post_list, name='my_post_list'),
    url(r'^accound/my/post/edit/(?P<post_id>\d+)$', views_accound.edit_my_post, name='edit_post'),

    # 文章分享部分
    url(r'^post/publish/page$', views_index.post_publish_page, name='post_publish_page'),
    url(r'^post/publish$', views_index.post_publish, name='post_publish'),
    url(r'^post/success$', views_index.post_success, name='post_success'),
    url(r'^post/show/(?P<post_id>\d+)/(?P<comment_page>\d+)$', views_index.post_show, name='post_show'),
    url(r'^post/comment$', views_index.post_comment, name='post_comment'),
    url(r'^post/comment/delete/(?P<comment_id>\d+)$', views_index.delete_comment, name='post_comment_delete'),
    url(r'^post/list/(?P<category_id>\d+)/(?P<page>\d+)$', views_index.post_list, name='post_list'),
    url(r'^post/image$', views_index.image_save, name='post_image_save'),
    url(r'^post/delete/(?P<post_id>\d+)$', views_index.delete_post, name='post_delete_post'),
]
