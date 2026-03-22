/**
 * AI 聊天悬浮窗交互逻辑
 * @Author: HeXW
 * @Date: 2026/3/18
 */

$(document).ready(function() {
    
    // 切换聊天面板
    $('#ai-chat-toggle').click(function() {
        $('#ai-chat-panel').toggleClass('hidden');
        if (!$('#ai-chat-panel').hasClass('hidden')) {
            $('#chat-input').focus();
        }
    });
    
    // 关闭按钮
    $('#ai-chat-close').click(function() {
        $('#ai-chat-panel').addClass('hidden');
    });
    
    // 发送按钮
    $('#chat-send').click(function() {
        sendMessage();
    });
    
    // 回车发送
    $('#chat-input').keypress(function(e) {
        if (e.which === 13) {
            sendMessage();
        }
    });
    
    // 发送消息函数
    function sendMessage() {
        var message = $('#chat-input').val().trim();
        if (!message) return;
        
        // 添加用户消息到聊天区
        addMessage('user', message);
        $('#chat-input').val('');
        
        // 显示加载中
        addMessage('ai', '思考中...', 'loading');
        
        // 获取当前页面上下文
        var context = getCurrentPageContext();
        
        // 调用后端 API
        $.ajax({
            url: '/ai/chat/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                message: message,
                context: context
            }),
            success: function(res) {
                // 移除加载中消息
                $('.message.loading').remove();
                
                if (res.status === 'success') {
                    addMessage('ai', res.reply);
                } else {
                    addMessage('ai', '出错了：' + (res.message || '未知错误'));
                }
            },
            error: function(xhr, status, error) {
                $('.message.loading').remove();
                var errorMsg = '网络错误';
                if (xhr.status === 0) {
                    errorMsg = '无法连接服务器，请检查服务是否运行';
                } else if (xhr.status === 500) {
                    errorMsg = '服务器内部错误';
                }
                addMessage('ai', errorMsg + ' (' + error + ')');
            }
        });
    }
    
    // 添加消息到聊天区
    function addMessage(role, text, type) {
        var avatar = role === 'user' ? '👤' : '🤖';
        var typeClass = type || '';
        
        var html = '<div class="message ' + role + ' ' + typeClass + '">' +
                   '<div class="avatar">' + avatar + '</div>' +
                   '<div class="content">' + escapeHtml(text) + '</div>' +
                   '</div>';
        
        $('#chat-messages').append(html);
        
        // 滚动到底部
        var messagesContainer = document.getElementById('chat-messages');
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    // HTML 转义（防止 XSS）
    function escapeHtml(text) {
        var div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML.replace(/\n/g, '<br>');
    }
    
    // 获取当前页面上下文
    function getCurrentPageContext() {
        var path = window.location.pathname;
        var context = null;
        
        if (path.includes('/case/list/')) {
            context = '当前在用例列表页';
        } else if (path.includes('/case/add/')) {
            context = '当前在新增用例页';
        } else if (path.includes('/project/list/')) {
            context = '当前在项目管理页';
        } else if (path.includes('/evn/list/')) {
            context = '当前在环境管理页';
        } else if (path.includes('/interface/list/')) {
            context = '当前在接口管理页';
        } else if (path.includes('/variable/list/')) {
            context = '当前在变量管理页';
        } else if (path === '/front/index/' || path === '/front/index') {
            context = '当前在首页（用例管理）';
        }
        
        return context;
    }
    
    // 页面加载时显示欢迎语
    setTimeout(function() {
        if (!$('#ai-chat-panel').hasClass('hidden')) {
            addMessage('ai', '你好！我是卡卡罗特 AI 助手 👊 有什么可以帮你的？');
        }
    }, 500);
});
