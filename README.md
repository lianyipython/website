# website  
使用Django框架搭建一个官方网站  
  
一 部署开发环境:  
1) 安装python3.6.X  
2）使用pip命令安装一下包:    
----- pip install django==1.11.2  
----- pip install pillow  
----- pip install django-tinymce  
  
二 设置项目信息    
1）使用Pycharm新建django项目    
2）选择zxr这个目录  
3）打开zxr/zxr/setting.py这个文件    
4）修改128行 MEDIA_ROOT 的值为 zxr/zxr_media 的实际位置  
  
三 设置启动信息    
1）在pycharm里->Run->Edit Configurations    
2) 新建一个django service服务 名字叫做 zxr ，默认设置就好  
3）执行Run/Run'zxr' ,便可运行项目  
