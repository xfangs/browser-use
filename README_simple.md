# Browser-Use 简化版 API

这是一个经过减配的 Browser-Use 多代理 HTTP API 服务，移除了复杂的 WebSocket 功能、多代理管理、日志广播等高级功能，只保留核心的浏览器自动化功能。

## 功能特性

- ✅ 简化的任务执行 API
- ✅ 基本的健康检查
- ✅ 浏览器会话复用
- ✅ LLM 实例复用
- ❌ 移除了 WebSocket 实时监控
- ❌ 移除了多代理管理
- ❌ 移除了复杂的日志广播

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动服务

```bash
python run_browser_use.py
```

服务将在 `http://localhost:8000` 启动。

### 3. 测试 API

```bash
python test_simple_api.py
```

## API 接口

### 健康检查

```
GET /health
```

返回服务状态信息。

### 执行任务

```
POST /run_task
```

请求体示例：

```json
{
  "task": "访问百度首页并搜索'Python'",
  "cdp_url": "http://127.0.0.1:9222",
  "model": "qwen2.5:7b",
  "host": "http://127.0.0.1:11434",
  "max_steps": 10,
  "headless": false,
  "verbose": true
}
```

## 配置说明

- `cdp_url`: Chrome DevTools Protocol 地址
- `model`: 使用的 LLM 模型名称
- `host`: Ollama 服务地址
- `task`: 要执行的任务描述
- `max_steps`: 最大执行步数
- `headless`: 是否无头模式运行浏览器
- `verbose`: 是否显示详细日志

## 前置条件

1. 启动 Chrome 浏览器并开启远程调试：

   ```bash
   chrome --remote-debugging-port=9222
   ```

2. 启动 Ollama 服务并加载模型：
   ```bash
   ollama serve
   ollama pull qwen2.5:7b
   ```

## 与完整版的区别

| 功能               | 完整版 | 简化版 |
| ------------------ | ------ | ------ |
| WebSocket 实时监控 | ✅     | ❌     |
| 多代理管理         | ✅     | ❌     |
| 日志广播           | ✅     | ❌     |
| 代理状态跟踪       | ✅     | ❌     |
| 任务队列管理       | ✅     | ❌     |
| 核心浏览器自动化   | ✅     | ✅     |
| HTTP API           | ✅     | ✅     |
| 健康检查           | ✅     | ✅     |

## 适用场景

- 只需要基本的浏览器自动化功能
- 不需要实时监控和状态跟踪
- 资源受限的环境
- 快速原型开发
- 学习和测试用途

## 故障排除

如果遇到问题，请检查：

1. Chrome 浏览器是否已启动并开启远程调试
2. Ollama 服务是否正常运行
3. 网络连接是否正常
4. 依赖包是否正确安装

