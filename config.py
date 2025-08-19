# -*- coding: utf-8 -*-
"""
配置文件：管理ChatOllama和浏览器的配置参数
"""

# Ollama配置
OLLAMA_CONFIG = {
    "host": "http://127.0.0.1:11434",  # Ollama服务地址
    "model": "qwen2.5:7b",             # 默认模型
    "timeout": 30                       # 请求超时时间（秒）
}

# 浏览器配置
BROWSER_CONFIG = {
    "cdp_url": "http://localhost:9222",  # Chrome DevTools Protocol地址
    "headless": False,                   # 是否无头模式
    "timeout": 300                       # 浏览器操作超时时间（秒）
}

# Agent配置
AGENT_CONFIG = {
    "max_steps": 10,                     # 最大执行步数
    "verbose": True,                     # 是否显示详细日志
    "retry_attempts": 3                  # 重试次数
}

# 任务配置
TASK_CONFIG = {
    "default_task": "访问百度首页并搜索'人工智能'",  # 默认任务
    "task_timeout": 600                  # 任务总超时时间（秒）
}
