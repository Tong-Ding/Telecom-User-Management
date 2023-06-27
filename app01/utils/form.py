# 开发时间 2022/9/13 10:33
# 文件: form.py
"""
该文件定义视图函数中的 ModelForm类方法
"""

from app01 import models
from django import forms
from django.core.validators import RegexValidator  # 正则
from django.core.exceptions import ValidationError  # 错误信息
from app01.utils.bootstrap import BootstrapModelForm, BootstrapForm  # 自定义BootstrapModelForm类
from app01.utils.encrypt import md5


class LoginForm(BootstrapForm):
    """登录ModelForm方法"""
    username = forms.CharField(
        label='username',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username'}),
        required=True,  # 验证 必填，默认不能为空
    )
    password = forms.CharField(
        label='password',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}, render_value=True),  # 失败不清空
        required=True
    )
    code = forms.CharField(
        label='code',
        widget=forms.TextInput,
        required=True
    )

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        return md5(pwd)


class AdminModelForm(BootstrapModelForm):
    """管理员的ModelForm方法"""
    confirm_password = forms.CharField(
        label='confirm password',
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ['username', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')

        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')  # 已经是md5
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("Passwords do not match")

        # 返回什么，此字段以后保存到数据库就是什么。
        return confirm


class AdminEditModelForm(BootstrapModelForm):
    """编辑管理员ModelForm"""

    class Meta:
        model = models.Admin
        fields = ['username']


class AdminResetModelForm(BootstrapModelForm):
    """重置管理员密码ModelForm"""
    confirm_password = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(render_value=True),
    )

    class Meta:
        model = models.Admin
        fields = ['password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        md5_pwd = md5(pwd)

        # 去数据库校验当前密码和新输入的密码是否一致
        exists = models.Admin.objects.filter(id=self.instance.pk, password=md5_pwd).exists()
        if exists:
            raise ValidationError('Cannot be the same as the previous password')

        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('password')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if confirm != pwd:
            raise ValidationError("Passwords do not match")

        # 返回什么，此字段以后保存到数据库就是什么。
        return confirm


class DepartModelForm(BootstrapModelForm):
    """部门的ModelForm方法"""

    class Meta:
        model = models.Department
        fields = ['title', ]


class UserModelForm(BootstrapModelForm):
    """用户的ModelForm方法"""
    name = forms.CharField(min_length=2, label='username')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'age', 'account', 'create_time', 'gender', 'depart']


class PrettyModelForm(BootstrapModelForm):
    """靓号的ModelForm方法"""
    # 验证方式1
    mobile = forms.CharField(
        label="mobile",
        validators=[RegexValidator(r'^1[3-9]\d{9}$', 'Invalid phone number format')],
        disabled=False,  # 设置为true,则按钮就会显示灰色不能点击
    )

    class Meta:
        model = models.PrettyNum
        fields = ['mobile', 'price', 'level', 'status']
        # fields = "__all__"

    # 验证方式2
    def clean_mobile(self):
        # 当前编辑的那一行id
        row_id = self.instance.pk
        text_mobile = self.cleaned_data["mobile"]

        exists = models.PrettyNum.objects.exclude(id=row_id).filter(mobile=text_mobile).exists()
        if exists:
            # 验证不通过
            raise ValidationError("The phone number already exists!")

        # 验证通过
        return text_mobile


class CityModelForm(BootstrapModelForm):
    """城市ModelForm"""
    bootstrap_exclude_fields = ['img']

    class Meta:
        model = models.City
        fields = '__all__'
