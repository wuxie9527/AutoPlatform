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
import threading
import os
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
    try:
        testEnvId = request.GET.get("evn_id")
        case_id = request.GET.get("case_id")
        if not case_id or not testEnvId:
            return JsonResponse({'success': False, 'error': '参数错误'})
        
        # 启动后台线程执行测试
        thread = threading.Thread(
            target=execute_test_in_background,
            args=(testEnvId, case_id),
            daemon=True
        )
        thread.start()

        return JsonResponse({
            'success': True,
            'message': '测试已开始执行',
            'case_id': case_id,
            'testEnvId': testEnvId
        })
    except Exception as e:
        logger.error(f"执行测试用例失败: {e}")
        return JsonResponse({'success': False, 'error': str(e)})



def execute_test_in_background(testEnvId, case_id):
    """
    后台线程执行测试用例的函数
    这里可以调用实际的测试执行逻辑，并将日志写入日志文件
    """
    case_list = models.test_case.objects.filter(id=case_id)
    test_object = models.evn_config.objects.filter(id=testEnvId).first()
    if not case_list:
        logger.error(f"测试用例不存在: case_id={case_id}")
        return
    logger.info(f"开始执行测试用例: 用例名称：{case_list[0].case_name}, 测试环境：{test_object.evn_name}")
    test_obj_data = {}
    test_obj_data['test_object'] = test_object.test_object_config
    test_obj_data['database_config'] = test_object.database_config
    cases = []
    for case in case_list[0].steps:
        interface_obj = models.interface.objects.get(id=case.get("interface_id"))
        request_header = models.variable.objects.get(var_type= "header",key=case.get("header"))
        step = {
            "步骤ID" : case.get("step_id"),
            "步骤名称": case["step_name"],
            "执行方式": case["method"],
            "url":  case["url"],
            "测试对象名称": case["object_name"],
            "header": request_header.value,
            "body": case["body"],
            "参数": case["params"],
            "接口校验": interface_obj.check_interface,
            "数据库校验": interface_obj.check_db,
            "变量输出": interface_obj.export_variable,
        }
        cases.append(step)
    debug_case(cases,test_obj_data,logger)
    return





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
            
            # 1. 发送连接成功消息
            yield self._format_sse_event('system', {
                'status': 'connected',
                'message': 'SSE连接已建立'
            })
            
            # 2. 发送历史日志（最后20行）
            history_logs = self._read_last_lines(5)
            for log in history_logs:
                yield self._format_sse_event('log', {
                    'type': 'history',
                    'content': log,
                })
                
            # 3. 实时监控新日志
            try:
                 # 第一次打开，移动到文件末尾
                with open(self.log_file, 'r', encoding='utf-8') as f:
                    f.seek(0, 2)  # 移动到文件末尾
                    last_position = f.tell()         
                inode = None
                retry_count = 0

                while True:
                    try:
                        # 检查文件是否存在
                        if not self.log_file.exists():
                            yield self._format_sse_event('warning', {
                                'message': f'日志文件不存在: {self.log_file}'
                            })
                            time.sleep(1)
                            continue

                        # 检查文件是否被轮转（inode变化）
                        current_inode = os.stat(self.log_file).st_ino
                        if inode is None:
                            inode = current_inode
                        elif inode != current_inode:
                            # 文件被轮转，重新开始
                            yield self._format_sse_event('system', {
                                'type': 'file_rotated',
                                'message': '检测到日志文件轮转'
                            })
                            inode = current_inode
                            last_position = 0

                        # 打开文件
                        with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
                            # 如果文件被截断，重置位置
                            f.seek(0, 2)
                            current_size = f.tell()
                            if current_size < last_position:
                                yield self._format_sse_event('system', {
                                    'type': 'file_truncated',
                                    'message': '检测到日志文件被清空'
                                })
                                last_position = 0

                            # 移动到上次读取的位置
                            f.seek(last_position)  # 从文件末尾开始读取

                            # 读取所有新行
                            new_lines = []
                            while True:
                                line = f.readline()
                                if not line:  # 没有更多新行
                                    break
                                if line.strip():  # 跳过空行
                                    new_lines.append(line.strip())

                            # 如果有新行，推送
                            if new_lines:
                                for line in new_lines:
                                    yield self._format_sse_event('log', {
                                        'type': 'realtime',
                                        'content': line,
                                    })
                                retry_count = 0  # 重置重试计数
                            else:
                                # 没有新内容，发送心跳
                                retry_count += 1
                                if retry_count % 20 == 0:  # 每20次心跳发送一次状态
                                    yield self._format_sse_event('heartbeat', {
                                        'count': retry_count,
                                        'position': last_position,
                                        'file_size': current_size
                                    })

                            # 更新最后位置
                            last_position = f.tell()

                        # 短时间等待
                        time.sleep(0.1)  # 降低CPU使用率

                    except (FileNotFoundError, PermissionError) as e:
                        # 文件操作异常
                        yield self._format_sse_event('error', {
                            'message': f'文件访问异常: {str(e)}'
                        })
                        time.sleep(2)

            except GeneratorExit:
                # 客户端断开连接
                print("客户端断开连接")
    
            except Exception as e:
                # 其他异常
                print(f"日志监控异常: {e}")
                yield self._format_sse_event('error', {
                    'message': f'监控进程异常: {str(e)}'
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
        return f"event: {event_type}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n"