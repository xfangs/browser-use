#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用Ollama的推理代码
"""

import asyncio
import os
from browser_use import Agent, BrowserSession
from browser_use.llm import ChatOllama


async def main():


    # 3. 连接到Chrome浏览器
    browser_session = BrowserSession(cdp_url="http://127.0.0.1:9222")

    initial_actions = [
        {'go_to_url': {'url': 'https://www.google.com', 'new_tab': True}}
    ]
    
    # 4. 创建Agent实例
    agent = Agent(
        task="用你的邮箱写一封邮件给我，内容是'你好'。你的邮箱：hyperagent.hypt@gmail.com，密码是：hyperagent0725，我的邮箱是marissa.mossai@gmail.com",
        initial_actions=initial_actions,
        llm=ChatOllama(host="http://127.0.0.1:11434", model="qwen2.5:7b"),
        browser_session=browser_session,
        use_vision=False,
    )
    
    # 5. 执行任务
    result = await agent.run()

    print(result)

    await asyncio.sleep(1000000)

    # 6. 清理资源
    await browser_session.close()

if __name__ == "__main__":
    asyncio.run(main())
