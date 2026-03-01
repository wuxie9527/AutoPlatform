from django.db import models


# Create your models here.


class project(models.Model):
    prj_id = models.AutoField(primary_key=True, null=False)
    prj_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.prj_id} - {self.prj_name} - {self.description}"

    class Meta:
        db_table = 'project'  # 明确指定表名
        verbose_name = '项目表'


class evn_config(models.Model):
    evn_name= models.CharField(max_length=50)
    project = models.ForeignKey(
        project,
        on_delete=models.CASCADE,
        related_name='environments',
        verbose_name='所属项目'
    )
    description = models.CharField(max_length=100,blank=True, null=True)
    test_object_config = models.JSONField(verbose_name='测试对象配置',blank=True, null=True,default=dict)
    database_config = models.JSONField(verbose_name='数据库配置',blank=True, null=True,default=dict)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'evn_config'  # 明确指定表名
        verbose_name = '环境配置'
        verbose_name_plural = '环境配置'
        # 同一项目下环境名称不能重复
        unique_together = ['project', 'evn_name']

class variable(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=100)
    TYPE_CHOICES = (
        ('val', '变量'),
        ('header', '请求头'),
    )
    var_type = models.CharField(max_length=20, verbose_name='变量类型', choices=TYPE_CHOICES)
    evn = models.ForeignKey(
        evn_config,
        on_delete=models.CASCADE,
        related_name='variables',
        verbose_name='所属环境'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'variable'  # 明确指定表名
        verbose_name = '变量'
        verbose_name_plural = '变量'

class interface(models.Model):
    interface_name = models.CharField(max_length=50)
    url = models.CharField(max_length=200)
    method_choices = (
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    )      
    method = models.CharField(max_length=10, choices=method_choices)
    header = models.CharField(verbose_name='请求头',max_length=50)  
    project = models.ForeignKey(
        project,
        on_delete=models.CASCADE,
        related_name='interfaces',
        verbose_name='所属项目'
    )
    body = models.JSONField(verbose_name='请求参数', blank=True, null=True, default=dict)
    test_object = models.CharField(verbose_name='测试对象', max_length=100)
    check_interface = models.CharField(verbose_name='校验接口', blank=True, null=True, max_length=50)
    check_db = models.CharField(verbose_name='校验数据库', blank=True, null=True)
    export_variable = models.CharField(verbose_name='输出变量', blank=True, null=True, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        db_table = 'interface'  # 明确指定表名
        verbose_name = '接口管理'
        verbose_name_plural = '接口管理'
        ordering = ['-created_at']

class test_case(models.Model):
    case_name = models.CharField(max_length=50)
    project = models.ForeignKey(
        project,
        on_delete=models.CASCADE,
        related_name='test_cases',
        verbose_name='所属项目'
    )
    description = models.CharField(max_length=100, blank=True, null=True)
    steps = models.JSONField(verbose_name='测试步骤', blank=True, null=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    def __str__(self):
        return self.case_name
    
    class Meta:
        db_table = 'test_case'  # 明确指定表名
        verbose_name = '测试用例'
        verbose_name_plural = '测试用例'
        ordering = ['-created_at']
