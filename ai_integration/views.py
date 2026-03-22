# coding=utf-8
"""
@Time : 2026/3/18 
@Author : HeXW
AI 集成视图
"""
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from .openclaw_client import chat_with_openclaw


@csrf_exempt
@require_http_methods(["POST"])
def ai_chat(request):
    """
    AI 聊天接口
    POST /ai/chat/
    
    Request:
    {
        "message": "用户消息",
        "context": "可选：当前页面上下文"
    }
    
    Response:
    {
        "status": "success|error",
        "reply": "AI 回复内容"
    }
    """
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        context = data.get('context', None)
        
        if not message:
            return JsonResponse({
                'status': 'error',
                'message': '消息不能为空'
            })
        
        # 调用 OpenClaw
        reply = chat_with_openclaw(message, context)
        
        return JsonResponse({
            'status': 'success',
            'reply': reply
        })
    
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': '无效的 JSON 格式'
        }, status=400)
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def ai_health(request):
    """
    AI 服务健康检查
    GET /ai/health/
    """
    return JsonResponse({
        'status': 'ok',
        'service': 'ai_integration'
    })
