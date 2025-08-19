# Browser-Use 异步推理 API 使用说明

## 概述

这个 API 已经改造为异步推理模式，支持：

- 🚀 异步任务提交和执行
- 📊 实时任务状态监控
- 🔄 后台任务处理
- 📈 任务进度跟踪
- 🧹 自动任务清理

## 主要改进

### 1. 异步任务执行

- 使用 `BackgroundTasks` 在后台异步执行任务
- 使用 `asyncio.run_in_executor` 将同步的 `agent.run()` 包装为异步
- 立即返回任务 ID，不阻塞 API 响应

### 2. 任务状态管理

- 全局任务状态存储
- 实时进度更新
- 详细的状态信息（pending, running, completed, failed）

### 3. 新增 API 接口

#### 提交异步任务

```http
POST /run_task
```

**请求参数：**

```json
{
  "cdp_url": "http://127.0.0.1:9222",
  "model": "qwen2.5:7b",
  "host": "http://127.0.0.1:11434",
  "task": "前往百度搜索人工智能相关信息",
  "max_steps": 20,
  "headless": false,
  "verbose": true,
  "timeout": 300
}
```

**响应：**

```json
{
  "success": true,
  "message": "任务已提交，任务ID: task_1234567890",
  "task_id": "task_1234567890"
}
```

#### 获取任务状态

```http
GET /task_status/{task_id}
```

**响应：**

```json
{
  "task_id": "task_1234567890",
  "status": "running",
  "progress": 0.6,
  "message": "开始执行任务...",
  "result": null,
  "error": null,
  "start_time": 1234567890.123,
  "end_time": null
}
```

#### 列出所有任务

```http
GET /list_tasks
```

**响应：**

```json
{
  "total": 3,
  "tasks": ["task_1", "task_2", "task_3"],
  "status_summary": {
    "pending": 1,
    "running": 1,
    "completed": 1,
    "failed": 0
  }
}
```

#### 清理已完成的任务

```http
DELETE /clear_completed_tasks
```

## 使用流程

### 1. 提交任务

```python
import requests

# 提交异步任务
response = requests.post("http://localhost:8000/run_task", json={
    "task": "前往百度搜索人工智能",
    "max_steps": 10,
    "headless": True
})

task_id = response.json()["task_id"]
print(f"任务已提交，ID: {task_id}")
```

### 2. 监控任务状态

```python
import time

while True:
    # 获取任务状态
    status_response = requests.get(f"http://localhost:8000/task_status/{task_id}")
    status_data = status_response.json()

    print(f"状态: {status_data['status']}, 进度: {status_data['progress']:.1%}")

    if status_data['status'] in ['completed', 'failed']:
        break

    time.sleep(2)  # 等待2秒后再次检查
```

### 3. 获取执行结果

```python
if status_data['status'] == 'completed':
    result = status_data['result']
    execution_time = status_data['end_time'] - status_data['start_time']
    print(f"任务完成！耗时: {execution_time:.2f}秒")
    print(f"结果: {result}")
else:
    error = status_data['error']
    print(f"任务失败: {error}")
```

## 测试

运行测试文件来验证异步推理功能：

```bash
python test_async_api.py
```

## 优势

1. **非阻塞 API**: 立即返回响应，不等待任务完成
2. **实时监控**: 可以实时查看任务执行进度
3. **资源管理**: 自动清理已完成的任务
4. **错误处理**: 详细的错误信息和状态跟踪
5. **可扩展性**: 支持多个任务并发执行

## 注意事项

1. 任务执行在后台进行，需要定期检查状态
2. 长时间运行的任务建议设置合理的超时时间
3. 定期清理已完成的任务以释放内存
4. 确保浏览器和 LLM 服务正常运行
