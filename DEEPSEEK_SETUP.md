# DeepSeek LLM 配置说明

## 概述

本项目已从 ChatOllama 迁移到 DeepSeek LLM，提供更强大的 AI 推理能力。

## 配置步骤

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

### 3. 创建.env 文件（推荐）

在项目根目录创建`.env`文件：

```env
# DeepSeek API配置
DEEPSEEK_API_KEY=your-actual-api-key-here
DEEPSEEK_BASE_URL=https://api.deepseek.com

# 浏览器配置
CHROME_DEBUG_PORT=9222

# 日志配置
LOG_LEVEL=INFO
```

## 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动 Chrome 调试模式

```bash
chrome --remote-debugging-port=9222
```

### 3. 运行程序

```bash
python run_browser_use.py
```

## 配置选项

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

## 安全注意事项

1. **API 密钥保护**: 不要在代码中硬编码 API 密钥
2. **环境隔离**: 为不同环境使用不同的 API 密钥
3. **访问控制**: 定期轮换 API 密钥
4. **监控使用**: 监控 API 调用量和费用
