#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用ChatOllama的最小化推理代码
"""

from browser_use import Agent, BrowserSession
from browser_use.llm import ChatOllama

def main():
    """主函数：演示最小化的推理流程"""
    
    # 1. 创建ChatOllama实例
    print("正在初始化ChatOllama...")
    llm = ChatOllama(
        host="http://127.0.0.1:11434",  # Ollama服务地址
        model="qwen2.5:7b"              # 使用的模型
    )
    
    # 2. 连接到Chrome浏览器
    print("正在连接浏览器...")
    browser_session = BrowserSession(cdp_url="http://localhost:9222")
    
    # 3. 创建Agent实例
    print("正在创建Agent...")
    agent = Agent(
        task="访问百度首页并搜索'人工智能'",  # 任务描述
        llm=llm,                           # LLM实例
        browser_session=browser_session,   # 浏览器会话
        verbose=True,                      # 显示详细日志
        max_steps=10                       # 最大执行步数
    )
    
    # 4. 执行任务
    print("开始执行任务...")
    try:
        result = agent.run()
        print(f"任务执行完成！结果: {result}")
    except Exception as e:
        print(f"任务执行失败: {e}")
    finally:
        # 5. 清理资源
        print("正在清理资源...")
        browser_session.close()

if __name__ == "__main__":
    main()
