#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的超时测试脚本
"""

import asyncio
import time

# 模拟超时配置
TASK_CONFIG = {
    "task_timeout": 5,  # 5秒超时用于测试
    "long_task_timeout": 10,
    "short_task_timeout": 3
}

async def simulate_long_task():
    """模拟一个长时间运行的任务"""
    print("开始执行长时间任务...")
    for i in range(10):
        print(f"步骤 {i+1}/10")
        await asyncio.sleep(1)  # 每个步骤1秒
    print("任务完成")
    return "任务成功"

async def test_timeout():
    """测试超时功能"""
    print("=== 超时测试开始 ===")
    
    try:
        # 使用5秒超时
        timeout = TASK_CONFIG["task_timeout"]
        print(f"设置超时时间: {timeout}秒")
        
        # 执行任务，如果超过5秒就超时
        result = await asyncio.wait_for(simulate_long_task(), timeout=timeout)
        print(f"任务结果: {result}")
        
    except asyncio.TimeoutError:
        print(f"任务超时！超过{timeout}秒")
    except Exception as e:
        print(f"任务执行失败: {e}")
    
    print("=== 超时测试结束 ===")

if __name__ == "__main__":
    asyncio.run(test_timeout())
