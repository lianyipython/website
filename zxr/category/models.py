from django.db import models


# 文章的分类
class Category(models.Model):
    name = models.CharField('分类名称',max_length=50)
    is_delete = models.BooleanField('标记为删除',default=False)
    is_default = models.BooleanField('标记为默认',default=False)
    order = models.IntegerField('排序',default=0)

    class Meta:
        verbose_name_plural = '分类'

    def __str__(self):
        return self.name