import json

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie

from front import forms, models


# Create your views here.


def index(request):
    return render(request, 'base.html/')


#项目管理
def project_list(request):
    if request.method == 'GET':
        data_dic = {}
        search_data = request.GET.get('q', '')
        if search_data:
            data_dic["mobile__contains"] = search_data
        querylist = models.project.objects.filter(**data_dic)
        return render(request, 'project/project_list.html', {"querylist": querylist})
    form = forms.projectModelForm(request.POST)
    if form.is_valid():
        form.save()
        return redirect('/front/project/list')


def project_delete(request, prj_id):
    print(prj_id)
    models.project.objects.filter(prj_id=prj_id).delete()
    return redirect('/front/project/list')

def project_edit(request,prj_id):
    row_object = models.project.objects.filter(prj_id=prj_id).first()
    if request.method == 'GET':
        querylist = models.project.objects.filter(prj_id=prj_id).first()
        return render(request,'project/project_edit.html' , {"querylist":querylist})
    form = forms.projectModelForm(request.POST, instance=row_object)
    if form.is_valid():
        form.save()
    return redirect('/front/project/list')



@csrf_exempt
def project_add(request):
    form = forms.projectModelForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"success":True,"status":200})
    return JsonResponse({"success":False, 'error':form.errors})

def project_select(request,prj_id):
    querylist = models.project.objects.filter(prj_id=prj_id).first()
    if not querylist:
        return JsonResponse({"status":False,"error":"数据不存在"})
    data = {
        'prj_id': querylist.prj_id,
        'prj_name': querylist.prj_name,
        'description': querylist.description,
    }
    return JsonResponse({"data":data,"status":200})


def project_edit(request):
    prj_id = request.GET.get("prj_id")
    row_object = models.project.objects.filter(prj_id=prj_id).first()
    if not row_object:
        return JsonResponse({"success": False, 'error': "数据错误"})
    form = forms.projectModelForm(request.POST, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": True, "status": 200})


#环境管理
def evn_list(request):
    project_list = models.project.objects.all()
    evn_querylist = models.evn_config.objects.filter()
    content = {
        "project_list":project_list,
        "evn_querylist":evn_querylist
    }
    return render(request, 'project/evn.html', content)


def evn_add(request):
    data = json.loads(request.body)
    form = forms.evnConfigModelForm(data)
    if form.is_valid():
        form.save()
    return JsonResponse(({"success": True, "status": 200}))


def evn_delete(request,evn_id):
    models.evn_config.objects.filter(id=evn_id).delete()
    return redirect('/front/evn/list')


def evn_select(request,evn_id):
    querylist = models.evn_config.objects.filter(id=evn_id).first()
    if not querylist:
        return JsonResponse({"status": False, "error": "数据不存在"})
    data = {
        'evn_name': querylist.evn_name,
        'project_id': querylist.project_id,
        "project_name" :querylist.project.prj_name,
        'description':querylist.description,
        'test_object_config': querylist.test_object_config,
        'database_config': querylist.database_config,
    }
    return JsonResponse({"data": data, "status": 200})

def evn_edit(request):
    evn_id = request.GET.get("evn_id")
    row_object = models.evn_config.objects.filter(id=evn_id).first()
    if not row_object:
        return JsonResponse({"success": False, 'error': "数据错误"})
    data = json.loads(request.body)
    form = forms.evnConfigModelForm(data, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": True, "status": 200})

#变量管理
def variable_list(request):
    variable_querylist = models.variable.objects.filter()
    evn_list = models.evn_config.objects.all()
    type_list = models.variable.TYPE_CHOICES
    content = {
        "variable_querylist": variable_querylist,
        "evn_list": evn_list,
        "type_list": type_list
    }
    return render(request, 'project/variable.html', content)

def variable_add(request):
    form = forms.variableModelForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": True, "status": 200})
    return JsonResponse({"success": False, "error": form.errors})

#接口管理
def interface_list(request):
    interface_querylist = models.interface.objects.filter()
    evn_list = models.evn_config.objects.values_list("test_object_config", flat=True)
    type_list = models.interface.method_choices
    header_list = models.variable.objects.values_list("key", flat=True).filter(var_type="header")
    project_list = models.project.objects.all()
    content = {
        "interface_querylist": interface_querylist,
        "test_object_list": evn_list,
        "type_list": type_list,
        "header_list": header_list,
        "project_list": project_list
    }
    return render(request, 'project/interface.html', content)

def interface_add(request):
    form = forms.interfaceModelForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": True, "status": 200})
    return JsonResponse({"success": False, "error": form.errors})