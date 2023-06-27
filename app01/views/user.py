# 开发时间 2022/9/13 10:37
# 文件: user.py
"""
用户 视图函数
"""
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination  # 自定义的分页组件
from app01.utils.form import UserModelForm


def user_list(request):
    """用户列表"""

    # 获取所有用户列表 [obj,obj,obj,]
    queryset = models.UserInfo.objects.all()
    """
    # 用Python的语法获取数据
    for obj in queryset:
        print(obj.id, obj.name, obj.account, obj.create_time.strftime("%Y-%m-%d"), obj.gender, obj.get_gender_display(), obj.depart_id, obj.depart.title)
        # obj.depart_id  # 获取数据库中存储的那个字段值
        # obj.depart.title  # 根据id自动去关联的表中获取那一行数据depart对象
    """

    # 分页
    page_object = Pagination(request, queryset)

    return render(request, 'user_list.html', {"queryset": page_object.page_queryset, "page_string": page_object.html()})


def user_add(request):
    """添加用户（ModelForm版本）"""
    title = 'Add user'
    if request.method == "GET":
        form = UserModelForm
        return render(request, 'user_change.html', {"form": form, 'title': title})

    # 用户POST提交数据，数据校验
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()
        return redirect('/user/list/')

    # 校验失败，在页面上显示错误信息
    return render(request, 'user_change.html', {"form": form, 'title': title})


def user_edit(request, nid):
    """编辑用户"""
    title = 'Edit User'
    # 根据id去数据库获取要编辑的那一行数据（对象）
    row_object = models.UserInfo.objects.filter(id=nid).first()

    if request.method == "GET":
        form = UserModelForm(instance=row_object)
        return render(request, 'user_change.html', {"form": form, 'title': title})

    form = UserModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 默认保存的是用户输入的所有数据，如果想要在用户输入以外增加一点值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list')
    return render(request, 'user_change.html', {"form": form, 'title': title})


def user_delete(request, nid):
    """删除用户"""
    models.UserInfo.objects.filter(id=nid).delete()
    return redirect('/user/list')
