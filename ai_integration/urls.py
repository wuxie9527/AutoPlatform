# coding=utf-8
"""
@Time : 2026/3/18 
@Author : HeXW
AI 集成路由
"""
from django.urls import path
from . import views

app_name = 'ai_integration'

urlpatterns = [
    path('chat/', views.ai_chat, name='ai_chat'),
    path('health/', views.ai_health, name='ai_health'),
]
