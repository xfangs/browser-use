# Browser-Use Multi-Agent HTTP API

这是一个基于 Browser-Use 的多 Agent HTTP 接口服务，支持创建、管理和运行多个浏览器自动化 Agent。

## 功能特性

- 🚀 支持多 Agent 并发运行
- 🌐 HTTP REST API 接口
- 🔌 WebSocket 实时监控推理过程
- 🔄 可配置的浏览器会话和 LLM 实例
- 📝 灵活的任务参数配置
- 🏥 健康检查接口

## 安装依赖

```bash
pip install -r requirements.txt
```

## 启动服务

```bash
python run_browser_use.py
```

服务将在 `http://localhost:8000` 启动。

## API 接口说明

### 1. 创建 Agent

**POST** `/create_agent`

创建新的 Agent 实例。

**请求参数：**

```json
{
  "cdp_url": "http://127.0.0.1:9222",
  "model": "qwen2.5:7b",
  "host": "http://127.0.0.1:11434",
  "task": "前往百度搜索人工智能相关信息",
  "max_steps": 20,
  "headless": false,
  "verbose": true
}
```

**响应：**

```json
{
  "success": true,
  "message": "Agent agent_1_1234567890 创建成功",
  "result": {
    "agent_id": "agent_1_1234567890"
  }
}
```

### 2. 运行 Agent

**POST** `/run_agent/{agent_id}`

运行指定的 Agent。

**响应：**

```json
{
  "success": true,
  "message": "Agent agent_1_1234567890 运行完成",
  "result": "任务执行结果..."
}
```

### 3. 直接运行任务

**POST** `/run_task`

创建临时 Agent 并立即执行任务，执行完成后自动清理。

**请求参数：** 同创建 Agent 接口

### 4. 列出所有 Agent

**GET** `/list_agents`

获取当前所有活跃的 Agent 列表。

**响应：**

```json
{
  "success": true,
  "message": "当前有 2 个活跃Agent",
  "result": {
    "agents": ["agent_1_1234567890", "agent_2_1234567891"]
  }
}
```

### 5. 移除 Agent

**DELETE** `/remove_agent/{agent_id}`

移除指定的 Agent。

### 6. 健康检查

**GET** `/health`

检查服务状态和活跃 Agent 数量。

### 7. WebSocket 实时监控

**WebSocket** `/ws/{agent_id}`

通过 WebSocket 实时监控指定 Agent 的推理过程。

**连接示例：**

```javascript
const ws = new WebSocket("ws://localhost:8000/ws/agent_1_1234567890");
ws.onmessage = function (event) {
  const data = JSON.parse(event.data);
  console.log("收到消息:", data);
};
```

**消息类型：**

- `connection`: 连接状态消息
- `status`: Agent 状态更新
- `log`: 推理过程日志
- `step`: 执行步骤信息
- `error`: 错误信息
- `warning`: 警告信息
- `pong`: 心跳响应

## 使用示例

### 使用 curl 创建并运行 Agent

```bash
# 1. 创建Agent
curl -X POST "http://localhost:8000/create_agent" \
  -H "Content-Type: application/json" \
  -d '{
    "cdp_url": "http://127.0.0.1:9222",
    "model": "qwen2.5:7b",
    "host": "http://127.0.0.1:11434",
    "task": "前往百度搜索人工智能相关信息"
  }'

# 2. 运行Agent（使用返回的agent_id）
curl -X POST "http://localhost:8000/run_agent/agent_1_1234567890"

# 3. 直接运行任务
curl -X POST "http://localhost:8000/run_task" \
  -H "Content-Type: application/json" \
  -d '{
    "cdp_url": "http://127.0.0.1:9222",
    "model": "qwen2.5:7b",
    "host": "http://127.0.0.1:11434",
    "task": "前往百度搜索人工智能相关信息"
  }'
```

### 使用 Python 客户端

```python
import requests
import json

# 创建Agent
response = requests.post(
    "http://localhost:8000/create_agent",
    json={
        "cdp_url": "http://127.0.0.1:9222",
        "model": "qwen2.5:7b",
        "host": "http://127.0.0.1:11434",
        "task": "前往百度搜索人工智能相关信息"
    }
)

agent_data = response.json()
agent_id = agent_data["result"]["agent_id"]

# 运行Agent
run_response = requests.post(f"http://localhost:8000/run_agent/{agent_id}")
result = run_response.json()
print(result["result"])
```

## 参数说明

- **cdp_url**: Chrome DevTools Protocol URL，默认 `http://127.0.0.1:9222`
- **model**: Ollama 模型名称，默认 `qwen2.5:7b`
- **host**: Ollama 服务地址，默认 `http://127.0.0.1:11434`
- **task**: 任务描述（必须参数）
- **max_steps**: 最大执行步骤，默认 20
- **headless**: 是否无头模式，默认 false
- **verbose**: 是否启用详细日志，默认 true

## 注意事项

1. 确保 Chrome 浏览器已启动并开启远程调试模式
2. 确保 Ollama 服务正在运行
3. 每个 Agent 使用独立的浏览器会话和 LLM 实例
4. 任务完成后建议及时清理不需要的 Agent 以释放资源
5. WebSocket 连接支持多客户端同时监控同一个 Agent
6. 可以通过浏览器打开 `websocket_monitor.html` 进行可视化监控

## 监控工具

### WebSocket 客户端测试

```bash
python websocket_client.py
```

### 可视化监控界面

在浏览器中打开 `websocket_monitor.html` 文件，可以：

- 创建和管理 Agent
- 实时监控推理过程
- 查看详细的执行日志
- 可视化操作界面

## API 文档

启动服务后，访问 `http://localhost:8000/docs` 查看完整的 API 文档（Swagger UI）。
