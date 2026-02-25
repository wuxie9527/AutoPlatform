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




