# Browser-Use Multi-Agent HTTP API (DeepSeek 版本)

这是一个基于 Browser-Use 的多 Agent HTTP 接口服务，使用 **DeepSeek LLM** 提供强大的 AI 推理能力，支持创建、管理和运行多个浏览器自动化 Agent。

## 🆕 最新更新

- ✅ **已迁移到 DeepSeek LLM** - 告别本地 Ollama，享受云端 AI 能力
- 🚀 **更快的推理速度** - 云端 GPU 加速，响应更迅速
- 🌐 **无需本地部署** - 直接使用 DeepSeek API 服务
- 💰 **成本可控** - 按使用量付费，无需维护本地资源

## 功能特性

- 🚀 支持多 Agent 并发运行
- 🌐 HTTP REST API 接口
- 🔌 WebSocket 实时监控推理过程
- 🔄 可配置的浏览器会话和 LLM 实例
- 📝 灵活的任务参数配置
- 🏥 健康检查接口
- 🤖 **DeepSeek LLM 集成** - 强大的 AI 推理能力

## 快速开始

### 1. 获取 DeepSeek API 密钥

1. 访问 [DeepSeek 官网](https://platform.deepseek.com/)
2. 注册账号并登录
3. 在控制台中创建 API 密钥
4. 复制 API 密钥

### 2. 设置环境变量

#### Windows PowerShell

```powershell
$env:DEEPSEEK_API_KEY="your-actual-api-key-here"
```

#### Windows CMD

```cmd
set DEEPSEEK_API_KEY=your-actual-api-key-here
```

#### Linux/Mac

```bash
export DEEPSEEK_API_KEY="your-actual-api-key-here"
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 启动 Chrome 调试模式

```bash
chrome --remote-debugging-port=9222
```

### 5. 启动服务

#### 使用启动脚本（推荐）

```bash
# Windows
start_deepseek.bat

# PowerShell
.\start_deepseek.ps1
```

#### 直接运行

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
  "model": "deepseek-chat",
  "api_key": "your-deepseek-api-key",
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

### 5. 移除 Agent

**DELETE** `/remove_agent/{agent_id}`

移除指定的 Agent。

### 6. 健康检查

**GET** `/health`

检查服务状态和活跃 Agent 数量。

### 7. WebSocket 实时监控

**WebSocket** `/ws/{agent_id}`

实时监控指定 Agent 的执行过程。

## 配置说明

### 环境变量

| 变量名              | 说明                  | 默认值                   |
| ------------------- | --------------------- | ------------------------ |
| `DEEPSEEK_API_KEY`  | DeepSeek API 密钥     | 必需                     |
| `DEEPSEEK_BASE_URL` | DeepSeek API 基础 URL | https://api.deepseek.com |
| `CHROME_DEBUG_PORT` | Chrome 调试端口       | 9222                     |
| `LOG_LEVEL`         | 日志级别              | INFO                     |

### 模型参数

| 参数          | 说明              | 默认值           |
| ------------- | ----------------- | ---------------- |
| `model`       | 使用的模型名称    | deepseek-chat    |
| `temperature` | 生成温度          | 0.7              |
| `max_tokens`  | 最大生成 token 数 | 根据模型自动设置 |

## 前置条件

1. **DeepSeek API 密钥**: 有效的 DeepSeek API 密钥
2. **Chrome 浏览器**: 以调试模式启动
   ```bash
   chrome --remote-debugging-port=9222
   ```
3. **网络连接**: 能够访问 DeepSeek API 服务

## 与 Ollama 版本的区别

| 功能     | Ollama 版本    | DeepSeek 版本 |
| -------- | -------------- | ------------- |
| LLM 服务 | 本地部署       | 云端 API      |
| 模型管理 | 需要下载模型   | 无需管理模型  |
| 推理速度 | 依赖本地硬件   | 云端 GPU 加速 |
| 维护成本 | 需要维护服务器 | 按使用量付费  |
| 扩展性   | 受本地资源限制 | 云端弹性扩展  |

## 故障排除

### 常见问题

1. **API 密钥错误**

   - 确保环境变量正确设置
   - 检查 API 密钥是否有效
   - 验证账户余额

2. **网络连接问题**

   - 检查网络连接
   - 确认防火墙设置
   - 尝试使用代理

3. **浏览器连接失败**
   - 确保 Chrome 以调试模式启动
   - 检查端口是否被占用
   - 验证 Chrome 版本兼容性

### 调试模式

设置更详细的日志级别：

```bash
$env:LOG_LEVEL="DEBUG"
python run_browser_use.py
```

## 性能优化

1. **批量请求**: 合理设置`max_steps`参数
2. **缓存策略**: 利用 browser-use 的会话复用功能
3. **并发控制**: 避免同时运行过多任务
4. **API 调用优化**: 合理设置 temperature 和 max_tokens 参数

## 安全注意事项

1. **API 密钥保护**: 不要在代码中硬编码 API 密钥
2. **环境隔离**: 为不同环境使用不同的 API 密钥
3. **访问控制**: 定期轮换 API 密钥
4. **监控使用**: 监控 API 调用量和费用
5. **网络安全**: 确保网络连接安全

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
