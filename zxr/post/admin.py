from django.contrib import admin
from .models import Post, Comment

admin.site.site_header = "影评分享管理平台"


# 用户记录美食分享文章评论的数目
def post_comment_count(post):
    return post.comment_set.count()


# 设置别名，增加可读性
post_comment_count.short_description = '评论数'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # 后台列表要显示的字段
    list_display = (
        'order',
        'title',
        'category',
        post_comment_count,
        'author',
        'modify_date',
        'is_delete',
        'check',
        'go_index',
    )

    # 后台列表可以编辑的字段
    list_editable = (
        'category',
        'is_delete',
        'check',
        'go_index',
    )
    list_display_links = ('title',)

    # 排序
    ordering = ('-id', 'order')
    search_fields = ['title']

    # 过滤
    list_filter = ('is_delete', 'check', 'go_index')

    # 每隔列表显示的项目数量
    list_per_page = 10


# 评论在后台显示时，取出html标签
def no_html_content(comment):
    return comment.no_html_content()


no_html_content.short_description = '评论内容'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # 后台需显示的字段
    list_display = (
        no_html_content,
        'author',
        'create_date',
        'is_delete',
    )

    # 后台列表可以编辑的字段
    list_editable = (
        'is_delete',
    )

    # 排序
    ordering = ('-id',)
    search_fields = ['content']

    # 过滤
    list_filter = ('is_delete',)

    # 每隔列表显示的项目数量
    list_per_page = 10
