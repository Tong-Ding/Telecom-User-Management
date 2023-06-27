from django.db import models

# Create your models here.


class Admin(models.Model):
    """管理员表"""
    username = models.CharField(verbose_name='username', max_length=32)
    password = models.CharField(verbose_name='password', max_length=64)


class Department(models.Model):
    """部门表"""
    title = models.CharField(verbose_name='title', max_length=32)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """员工表"""
    name = models.CharField(verbose_name='name', max_length=16)
    password = models.CharField(verbose_name='password', max_length=64)
    age = models.IntegerField(verbose_name='age')
    account = models.DecimalField(verbose_name='Account balance', max_digits=10, decimal_places=2, default=0)
    create_time = models.DateField(verbose_name='Date of entry')

    # 无约束
    # depart_id = models.BigIntegerField(verbose_name='部门id')

    # 1.有约束
    #   -to,与那张表关联
    #   -to_field,表中的那一列关联
    # 2.Django自动
    #   -写的depart
    #   -生成数据列 depart_id
    # 3.部门表被删除
    #  3.1 级联删除  on_delete=models.CASCADE  表示如果部门表被删除，旗下的部门表的员工也被删除
    depart = models.ForeignKey(verbose_name='depart', to='Department', to_field='id', on_delete=models.CASCADE)
    #  3.2 置空  null=True, blank=True, on_delete=models.SET_NULL 表示如果部门表被删除，旗下的部门表的员工部门位为空值
    # depart = models.ForeignKey(to='Department', to_field='id', null=True, blank=True, on_delete=models.SET_NULL)

    # 在Django中做的约束
    gender_choices = (
        (1, 'Male'),
        (2, 'Female'),
    )
    gender = models.SmallIntegerField(verbose_name='gender', choices=gender_choices)


class PrettyNum(models.Model):
    """靓号表"""
    mobile = models.CharField(verbose_name="mobile", max_length=11)
    price = models.IntegerField(verbose_name="price", default=0)

    level_choices = (
        (1, 'Level 1'),
        (2, 'Level 2'),
        (3, 'Level 3'),
        (4, 'Level 4'),
    )
    level = models.SmallIntegerField(verbose_name="level", choices=level_choices, default=1)

    status_choices = (
        (1, 'Used'),
        (2, 'Unused'),
    )
    status = models.SmallIntegerField(verbose_name="status", choices=status_choices, default=2)


class City(models.Model):
    """城市表"""
    name = models.CharField(verbose_name='name', max_length=32)
    count = models.IntegerField(verbose_name='population')
    img = models.FileField(verbose_name='Logo', max_length=128, upload_to='city/')  # FillField即上传文件

