from django.http import StreamingHttpResponse, HttpResponse
from django.views import View
from pathlib import Path
import time
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt,ensure_csrf_cookie
from front import forms, models
import logging
import json

logger = logging.getLogger('django')
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
    print(form)
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

#测试用例管理
def case_list(request):
    interface_list = models.interface.objects.all()
    test_object_list = models.evn_config.objects.values_list("test_object_config", flat=True)
    type_list = models.interface.method_choices
    project_list = models.project.objects.all()
    evn_list =models.evn_config.objects.all()
    content = {
        "interface_querylist": interface_list,
        "case_querylist": models.test_case.objects.all(),
        "test_object_list": test_object_list,
        "type_list": type_list,
        "project_list": project_list,
        "evn_list": evn_list
    }
    return render(request, 'project/test_case.html', content)

def case_add(request):
    data = json.loads(request.body)
    form = forms.testCaseModelForm(data)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": True, "status": 200})
    return JsonResponse({"success": False, "error": form.errors})

def case_select(request,case_id):
    querylist = models.test_case.objects.filter(id=case_id).first()
    if not querylist:
        return JsonResponse({"status": False, "error": "数据不存在"})
    data = {
        'case_name': querylist.case_name,
        'project_id': querylist.project_id,
        "project_name" :querylist.project.prj_name,
        'description': querylist.description,
        'steps': querylist.steps
    }
    return JsonResponse({"data": data, "status": 200})

def case_edit(request):
    case_id = request.GET.get("case_id")
    row_object = models.test_case.objects.filter(id=case_id).first()
    if not row_object:
        return JsonResponse({"success": False, 'error': "数据错误"})
    data = json.loads(request.body)
    form = forms.testCaseModelForm(data, instance=row_object)
    if form.is_valid():
        form.save()
        return JsonResponse({"success": True, "status": 200})

def case_run(request):
    data = json.loads(request.body)
    case_id = data.get("case_id")
    # 这里可以调用测试执行逻辑，暂时模拟执行结果
    logger.info(f"开始执行测试用例ID: {case_id}")
    time.sleep(2)  # 模拟执行时间
    logger.info(f"完成执行测试用例ID: {case_id}")
    return JsonResponse({"success": True, "status": 200, "message": f"测试用例ID {case_id} 执行完成"})



class LogStreamView(View):
    """
        日志流视图
        读取日志文件并实时推送到前端
    """
    def __init__(self):
        # 日志文件路径
        self.log_file = Path("logs/front.log")
        # 确保日志目录存在
        self.log_file.parent.mkdir(exist_ok=True)

    def get(self, request):
        """
        处理SSE连接请求
        前端通过 EventSource('/api/logs/stream/') 连接到这里
        """
        
        def log_generator():
            """
            日志生成器
            这个函数会被StreamingHttpResponse调用
            """
            print(f"新的SSE连接建立: {request.META.get('REMOTE_ADDR')}")
            
            try:
                # 1. 发送连接成功消息
                yield self._format_sse_event('system', {
                    'status': 'connected',
                    'message': 'SSE连接已建立'
                })
                
                # 2. 发送历史日志（最后20行）
                history_logs = self._read_last_lines(20)
                for log in history_logs:
                    yield self._format_sse_event('log', {
                        'type': 'history',
                        'content': log,
                        'timestamp': time.time()
                    })
                
                # 3. 实时监控新日志
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    # 移动到文件末尾
                    f.seek(0, 2)
                    
                    # 记录心跳次数
                    heartbeat_count = 0
                    
                    while True:
                        # 尝试读取新行
                        line = f.readline()
                        
                        if line:
                            # 有新日志，推送到前端
                            yield self._format_sse_event('log', {
                                'type': 'realtime',
                                'content': line.strip(),
                                'timestamp': time.time()
                            })
                        else:
                            # 没有新日志，发送心跳保持连接
                            heartbeat_count += 1
                            if heartbeat_count % 10 == 0:  # 每10次心跳发送一次状态
                                yield self._format_sse_event('system', {
                                    'type': 'heartbeat',
                                    'count': heartbeat_count
                                })
                            else:
                                yield ": heartbeat\\n\\n"
                            
                            # 短暂等待
                            time.sleep(0.5)
                            
            except GeneratorExit:
                # 生成器被外部关闭（通常是客户端断开）
                print("客户端断开连接")
            except Exception as e:
                # 其他异常
                print(f"日志生成器异常: {e}")
                yield self._format_sse_event('error', {
                    'message': str(e)
                })
        
        # 创建流式响应
        response = StreamingHttpResponse(
            log_generator(),
            content_type='text/event-stream'
        )
        
        # 重要：设置HTTP头
        response['Cache-Control'] = 'no-cache'
        response['X-Accel-Buffering'] = 'no'
        
        return response

    def _read_last_lines(self, count):
        """读取最后N行日志"""
        if not self.log_file.exists():
            return []
        
        with open(self.log_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return [line.strip() for line in lines[-count:]] if lines else []

    def _format_sse_event(self, event_type, data):
        """格式化SSE事件"""
        return f"event: {event_type}\\ndata: {json.dumps(data, ensure_ascii=False)}\\n\\n"