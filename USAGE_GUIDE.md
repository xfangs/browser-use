# Browser-Use 优化使用指南

## 问题诊断

如果您遇到浏览器推理不能完整推理出结果的问题，可能的原因包括：

### 1. 步骤数不足
- **问题**：`max_steps` 设置过低，任务在完成前被中断
- **解决**：增加 `max_steps` 参数值

### 2. 超时时间过短
- **问题**：`timeout` 设置过短，复杂任务被强制中断
- **解决**：根据任务复杂度调整超时时间

### 3. 缺少重试机制
- **问题**：网络延迟或页面加载问题导致任务失败
- **解决**：启用重试机制，设置合适的重试次数

### 4. 任务完成状态未验证
- **问题**：任务看似完成但实际未达到预期结果
- **解决**：启用 `wait_for_completion` 和任务完成验证

## 优化配置参数

### 基础配置
```python
{
    "max_steps": 100,        # 增加默认最大步骤数
    "timeout": 300,          # 5分钟超时
    "retry_count": 3,        # 重试3次
    "wait_for_completion": True,  # 等待任务完成
    "verbose": True          # 启用详细日志
}
```

### 任务类型配置

#### 简单任务 (simple)
```python
{
    "max_steps": 50,
    "timeout": 180,
    "retry_count": 2,
    "wait_for_completion": True
}
```

#### 复杂任务 (complex)
```python
{
    "max_steps": 150,
    "timeout": 600,
    "retry_count": 5,
    "wait_for_completion": True
}
```

#### 研究任务 (research)
```python
{
    "max_steps": 200,
    "timeout": 900,
    "retry_count": 3,
    "wait_for_completion": True,
    "verbose": True
}
```

#### 快速任务 (quick)
```python
{
    "max_steps": 30,
    "timeout": 120,
    "retry_count": 1,
    "wait_for_completion": False,
    "headless": True
}
```

## 使用示例

### 1. 基本任务执行
```python
import requests

task_data = {
    "task": "访问百度首页并搜索'Python教程'",
    "max_steps": 80,
    "timeout": 300,
    "retry_count": 3,
    "wait_for_completion": True
}

response = requests.post("http://localhost:8000/run_task", json=task_data)
result = response.json()
print(f"执行步骤数: {result.get('steps_executed', 0)}")
print(f"执行时间: {result.get('execution_time', 0):.2f}秒")
```

### 2. 复杂任务执行
```python
task_data = {
    "task": "访问GitHub，搜索Python项目，查看前5个项目的README内容",
    "max_steps": 150,
    "timeout": 600,
    "retry_count": 5,
    "wait_for_completion": True,
    "verbose": True
}
```

### 3. 数据提取任务
```python
task_data = {
    "task": "访问新闻网站，提取今日头条新闻的标题和摘要",
    "max_steps": 120,
    "timeout": 450,
    "retry_count": 4,
    "wait_for_completion": True
}
```

## 环境变量配置

您可以通过环境变量来设置默认配置：

```bash
# 设置最大步骤数
export BROWSER_USE_MAX_STEPS=150

# 设置超时时间（秒）
export BROWSER_USE_TIMEOUT=600

# 设置重试次数
export BROWSER_USE_RETRY_COUNT=5

# 设置是否等待完成
export BROWSER_USE_WAIT_FOR_COMPLETION=true
```

## 故障排除

### 1. 检查服务状态
```bash
curl http://localhost:8000/health
```

### 2. 查看详细日志
确保 `verbose: true` 已启用，查看控制台输出的详细执行信息。

### 3. 监控执行过程
- 观察步骤执行数量
- 检查是否有错误或警告信息
- 验证任务完成状态

### 4. 调整参数
根据任务复杂度和执行情况，动态调整：
- `max_steps`：如果任务经常在完成前停止
- `timeout`：如果任务经常超时
- `retry_count`：如果任务经常因临时问题失败

## 最佳实践

### 1. 任务描述优化
- 使用清晰、具体的任务描述
- 包含期望的结果或目标
- 指定具体的操作步骤

### 2. 参数配置策略
- 简单任务：使用较低的步骤数和超时时间
- 复杂任务：使用较高的步骤数和超时时间
- 数据密集型任务：增加超时时间和重试次数

### 3. 监控和调试
- 启用详细日志记录
- 监控执行时间和步骤数
- 分析失败原因并调整参数

### 4. 资源管理
- 及时清理不需要的浏览器会话
- 监控内存和CPU使用情况
- 避免同时运行过多复杂任务

## 常见问题解答

### Q: 任务总是超时怎么办？
A: 增加 `timeout` 参数值，或者将复杂任务分解为多个简单任务。

### Q: 任务执行步骤数不够怎么办？
A: 增加 `max_steps` 参数值，或者优化任务描述使其更清晰。

### Q: 如何提高任务成功率？
A: 启用重试机制，增加 `retry_count`，并确保 `wait_for_completion` 为 true。

### Q: 任务执行很慢怎么办？
A: 检查网络连接，考虑使用无头模式 (`headless: true`)，或者优化任务复杂度。

### Q: 如何调试任务执行问题？
A: 启用详细日志 (`verbose: true`)，观察执行步骤，检查错误信息。

## 联系支持

如果问题仍然存在，请：
1. 检查日志文件中的错误信息
2. 验证浏览器和LLM服务状态
3. 尝试使用不同的任务参数配置
4. 提供详细的错误信息和任务描述
