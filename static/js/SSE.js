
// 全局变量
let eventSource = null;  // SSE连接对象

// 1. 建立SSE连接
function connectSSE() {
    // 如果已连接，先断开
    if (eventSource) {
        disconnectSSE();
    }

    // 更新状态
    // updateStatus('connecting', '连接中...');

    // 创建EventSource对象
    // 这里连接到Django的SSE端点
    eventSource = new EventSource('/front/logs/stream/');

    // 2. 监听连接打开事件
    eventSource.onopen = function(event) {
        console.log('SSE连接已打开');
        // updateStatus('connected', '已连接');
    };

    // 3. 监听系统事件（连接成功、心跳等）
    eventSource.addEventListener('system', function(event) {
        const data = JSON.parse(event.data);
        console.log('系统事件:', data);
        // 添加到页面
        addLog(data.message, data.type);

        if (data.status === 'connected') {
            addLog(`✅ ${data.message}`, 'system');
        } else if (data.type === 'heartbeat') {
            // 心跳，不显示在界面上
            console.log(`心跳 ${data.count}`);
        }
    });

    // 4. 监听日志事件（核心）
    eventSource.addEventListener('log', function(event) {
        const data = JSON.parse(event.data);

        // 添加到页面
        addLog(data.content, data.type);
    });

    // 5. 监听错误事件
    eventSource.addEventListener('error', function(event) {
        const data = JSON.parse(event.data);
        console.error('错误事件:', data);
        addLog(`❌ ${data.message}`, 'error');
    });

    // 6. 监听SSE错误（连接级别）
    eventSource.onerror = function(event) {
        console.error('SSE连接错误:', event);

        if (eventSource.readyState === EventSource.CLOSED) {
            // updateStatus('disconnected', '连接断开');
            addLog('🔌 连接已断开', 'system');

            // 3秒后自动重连
            setTimeout(function() {
                addLog('🔄 尝试重新连接...', 'system');
                connectSSE();
            }, 3000);
        }
    };
}

// 断开SSE连接
function disconnectSSE() {
    if (eventSource) {
        eventSource.close();
        eventSource = null;
        // updateStatus('disconnected', '已断开');
        addLog('手动断开连接', 'system');
    }
}


// 添加日志到页面
function addLog(content, type = 'realtime') {
    const container = document.getElementById('run_case_result');
    container.value += content + '\n';

    // 自动滚动到底部
    container.scrollTop = container.scrollHeight;
    }

// 页面关闭时断开连接
window.addEventListener('beforeunload', function() {
    disconnectSSE();
});