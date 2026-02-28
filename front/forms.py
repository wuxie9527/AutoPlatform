# coding=utf-8
"""
@Time : 2026/2/6 下午9:52
@Author : HeXW
"""
from django import forms
from front.models import *
from django.core.validators import RegexValidator, ValidationError


class projectModelForm(forms.ModelForm):
    class Meta:
        model = project

        fields = ['prj_name', 'description']
        # fields = '__all__'


class evnConfigModelForm(forms.ModelForm):
    class Meta:
        model = evn_config
        fields = '__all__'


class variableModelForm(forms.ModelForm):
    class Meta:
        model = variable
        fields = '__all__'

class interfaceModelForm(forms.ModelForm):
    class Meta:
        model = interface
        fields = '__all__'

    def __str__(self):
        return super().__str__()