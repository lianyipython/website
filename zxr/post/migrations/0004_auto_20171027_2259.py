# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 14:59
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20171027_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='回帖者'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(verbose_name='评论内容'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='回帖时间'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='标记为删除'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='发布者'),
        ),
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.Category', verbose_name='分类'),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(verbose_name='文章内容'),
        ),
        migrations.AlterField(
            model_name='post',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='post',
            name='is_delete',
            field=models.BooleanField(default=False, verbose_name='标记为删除'),
        ),
        migrations.AlterField(
            model_name='post',
            name='modify_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='修改时间'),
        ),
        migrations.AlterField(
            model_name='post',
            name='order',
            field=models.IntegerField(default=0, verbose_name='排序'),
        ),
        migrations.AlterField(
            model_name='post',
            name='pv',
            field=models.IntegerField(default=1, verbose_name='浏览量'),
        ),
    ]
