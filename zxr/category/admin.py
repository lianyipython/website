from django.contrib import admin
from .models import Category


# 合计出某个分类的所有数据
def post_count(category):
    return category.post_set.count()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', post_count, 'order')
