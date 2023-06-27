# 开发时间 2022/9/13 10:37
# 文件: pretty.py
"""
靓号 视图函数
"""
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.pagination import Pagination  # 自定义的分页组件
from app01.utils.form import PrettyModelForm


def pretty_list(request):
    """靓号列表"""

    # 搜索
    mobile = request.GET.get("sc_mobile", '')
    level = request.GET.get("sc_level", '')
    date_dict = {}
    if mobile:
        date_dict["mobile__contains"] = mobile
    if level:
        date_dict['level__contains'] = level

    queryset = models.PrettyNum.objects.filter(**date_dict).order_by("-level")

    # 分页
    page_object = Pagination(request, queryset)

    context = {
        "mobile": mobile,
        "level": level,
        "queryset": page_object.page_queryset,  # 分完页的数据
        "page_string": page_object.html()  # 页码
    }

    return render(request, "pretty_list.html", context)


def pretty_add(request):
    """添加靓号"""
    title = 'Add pretty number'
    if request.method == "GET":
        form = PrettyModelForm
        return render(request, "change.html", {"form": form, 'title': title})

    form = PrettyModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, "change.html", {"form": form, 'title': title})


def pretty_edit(request, nid):
    """修改靓号"""
    title = 'Edit pretty number'
    row_object = models.PrettyNum.objects.filter(id=nid).first()

    if request.method == 'GET':
        form = PrettyModelForm(instance=row_object)
        return render(request, "change.html", {"form": form, 'title': title})

    form = PrettyModelForm(data=request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return redirect('/pretty/list/')

    return render(request, 'change.html', {"form": form, 'title': title})


def pretty_delete(request, nid):
    """删除靓号"""
    models.PrettyNum.objects.filter(id=nid).delete()
    return redirect('/pretty/list/')
