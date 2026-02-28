# coding=utf-8
"""
@Time : 2026/2/9 下午8:30
@Author : HeXW
"""
from django.contrib import admin
from django.urls import path

from front import views



urlpatterns = [
    #首页
    path('index/', views.index),
    #项目管理
    path('project/list/', views.project_list,name='project_list'),
    path('project/delete/<int:prj_id>/', views.project_delete),
    # path('project/edit/<int:prj_id>/', views.project_edit),
    path('project/add/', views.project_add, name='project_add'),
    path('project/select/<int:prj_id>/', views.project_select),
    path('project/edit/', views.project_edit),
    #环境管理
    path('evn/list/', views.evn_list),
    path('evn/add/', views.evn_add),
    path('evn/delete/<int:evn_id>/', views.evn_delete),
    path('evn/select/<int:evn_id>/', views.evn_select),
    path('evn/edit/', views.evn_edit),
    #变量管理
    path('variable/list/', views.variable_list),
    path('variable/add/', views.variable_add),
    # path('variable/delete/<int:var_id>/', views.variable_delete),
    # path('variable/select/<int:var_id>/', views.variable_select),
    # path('variable/edit/', views.variable_edit),
    #接口管理
    path('interface/list/', views.interface_list),
    path('interface/add/', views.interface_add),
    # path('interface/delete/<int:interface_id>/', views.interface_delete),
    # path('interface/select/<int:interface_id>/', views.interface_select),
    # path('interface/edit/', views.interface_edit),

]
