# coding=utf-8
"""
@Time : 2026/3/18 
@Author : HeXW
OpenClaw 客户端封装 - 通过 subprocess 调用 openclaw CLI
"""
import subprocess
import json
import os
import hashlib

# 固定的会话 ID（基于平台名称生成）
SESSION_ID = "autoplatform_ai_" + hashlib.md5(b"autoplatform").hexdigest()[:8]

def chat_with_openclaw(message, context=None):
    """
    通过 subprocess 调用 openclaw agent 命令
    使用固定的 session-id 保持对话连续性
    """
    full_prompt = message
    if context:
        full_prompt = f"当前上下文：{context}\n\n用户问题：{message}"
    
    try:
        # 调用 openclaw agent 命令
        result = subprocess.run(
            [
                'openclaw', 'agent',
                '--session-id', SESSION_ID,
                '--message', full_prompt,
                '--json'
            ],
            capture_output=True,
            text=True,
            timeout=65,
            env={**os.environ}
        )
        
        if result.returncode == 0:
            try:
                output = json.loads(result.stdout)
                # JSON 结构：result.payloads[0].text
                payloads = output.get('result', {}).get('payloads', [])
                if payloads and len(payloads) > 0:
                    return payloads[0].get('text', 'AI 没有返回内容')
                return 'AI 没有返回内容'
            except json.JSONDecodeError:
                return result.stdout.strip()
        else:
            error_msg = result.stderr.strip()
            # 如果是 Gateway 失败，尝试本地模式
            if 'Gateway' in error_msg or 'falling back' in error_msg.lower():
                return _chat_local(full_prompt)
            return f"AI 执行出错：{error_msg}"
    
    except subprocess.TimeoutExpired:
        return "AI 思考超时了，请稍后再试"
    except FileNotFoundError:
        return "找不到 openclaw 命令，请检查是否已安装"
    except Exception as e:
        return f"发生错误：{str(e)}"


def _chat_local(message):
    """
    备用方案：本地嵌入式模式（需要 API key 在环境变量中）
    """
    try:
        result = subprocess.run(
            [
                'openclaw', 'agent',
                '--local',
                '--message', message,
                '--json'
            ],
            capture_output=True,
            text=True,
            timeout=65,
            env={**os.environ}
        )
        
        if result.returncode == 0:
            output = json.loads(result.stdout)
            return output.get('reply', 'AI 没有返回内容')
        else:
            return f"本地模式失败：{result.stderr.strip()}"
    except Exception as e:
        return f"本地模式也失败了：{str(e)}"