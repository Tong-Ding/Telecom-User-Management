# 开发时间 2022/9/14 20:44
# 文件: city.py
"""
城市 视图函数
"""
from django.shortcuts import render, redirect
from app01 import models
from app01.utils.form import CityModelForm


def city_list(request):
    """城市列表"""
    queryset = models.City.objects.all()
    return render(request, 'city_list.html', {'queryset': queryset})


def city_add(request):
    """添加城市"""
    if request.method == 'GET':
        form = CityModelForm
        return render(request, 'city_add.html', {'form': form})

    form = CityModelForm(data=request.POST, files=request.FILES)
    if form.is_valid():
        form.save()
        return redirect('/city/list/')
    return render(request, 'city_add.html', {'form': form})


