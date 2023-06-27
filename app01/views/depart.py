# 开发时间 2022/9/13 10:37
# 文件: depart.py
"""
部门 视图函数
"""
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination  # 自定义的分页组件
from app01.utils.form import DepartModelForm


def depart_list(request):
    """部门列表"""
    queryset = models.Department.objects.all()

    # 分页
    page_object = Pagination(request, queryset)

    return render(request, 'depart_list.html', {"queryset": page_object.page_queryset, "page_string": page_object.html()})


def depart_add(request):
    """添加部门"""
    title = 'Add Department'
    if request.method == 'GET':
        form = DepartModelForm()
        return render(request, 'change.html', {"form": form, 'title': title})

    # 用户POST提交数据，数据校验
    form = DepartModelForm(data=request.POST)
    if form.is_valid():
        # 如果数据合法，保存到数据库
        form.save()
        return redirect('/depart/list/')

    # 校验失败，在页面上显示错误信息
    return render(request, 'change.html', {"form": form, 'title': title})


def depart_delete(request, nid):
    """删除部门"""
    models.Department.objects.filter(id=nid).delete()
    return redirect('/depart/list/')


def depart_edit(request, nid):
    """修改部门"""
    title = 'Edit Department'
    # 根据id去数据库获取要编辑的那一行数据（对象）
    row_object = models.Department.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = DepartModelForm(instance=row_object)
        return render(request, 'change.html', {"form": form, 'title': title})

    form = DepartModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        # 校验成功
        form.save()
        return redirect('/depart/list/')

    # 校验失败，提示错误信息
    return render(request, 'change.html', {"form": form, 'title': title})
