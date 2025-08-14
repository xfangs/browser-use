#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Browser-Use Multi-Agent API 测试脚本
"""

import requests
import json
import time
from typing import Dict, Any

class BrowserUseAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json"
        })
    
    def test_health_check(self) -> bool:
        """测试健康检查接口"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 健康检查通过: {data}")
                return True
            else:
                print(f"❌ 健康检查失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 健康检查异常: {e}")
            return False
    
    def test_create_agent(self, task: str) -> str:
        """测试创建Agent接口"""
        try:
            payload = {
                "cdp_url": "http://127.0.0.1:9222",
                "model": "qwen2.5:7b",
                "host": "http://127.0.0.1:11434",
                "task": task,
                "max_steps": 10,
                "headless": True,
                "verbose": False
            }
            
            response = self.session.post(f"{self.base_url}/create_agent", json=payload)
            if response.status_code == 200:
                data = response.json()
                agent_id = data["result"]["agent_id"]
                print(f"✅ Agent创建成功: {agent_id}")
                return agent_id
            else:
                print(f"❌ Agent创建失败: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"❌ Agent创建异常: {e}")
            return None
    
    def test_list_agents(self) -> bool:
        """测试列出Agent接口"""
        try:
            response = self.session.get(f"{self.base_url}/list_agents")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 获取Agent列表成功: {data}")
                return True
            else:
                print(f"❌ 获取Agent列表失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ 获取Agent列表异常: {e}")
            return False
    
    def test_run_agent(self, agent_id: str) -> bool:
        """测试运行Agent接口"""
        try:
            print(f"🔄 开始运行Agent: {agent_id}")
            response = self.session.post(f"{self.base_url}/run_agent/{agent_id}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Agent运行完成: {data['message']}")
                if data.get("result"):
                    print(f"📋 执行结果: {data['result']}")
                return True
            else:
                print(f"❌ Agent运行失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ Agent运行异常: {e}")
            return False
    
    def test_run_task(self, task: str) -> bool:
        """测试直接运行任务接口"""
        try:
            payload = {
                "cdp_url": "http://127.0.0.1:9222",
                "model": "qwen2.5:7b",
                "host": "http://127.0.0.1:11434",
                "task": task,
                "max_steps": 5,
                "headless": True,
                "verbose": False
            }
            
            print(f"🔄 开始直接运行任务: {task[:50]}...")
            response = self.session.post(f"{self.base_url}/run_task", json=payload)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 任务运行完成: {data['message']}")
                if data.get("result"):
                    print(f"📋 执行结果: {data['result']}")
                return True
            else:
                print(f"❌ 任务运行失败: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            print(f"❌ 任务运行异常: {e}")
            return False
    
    def test_remove_agent(self, agent_id: str) -> bool:
        """测试移除Agent接口"""
        try:
            response = self.session.delete(f"{self.base_url}/remove_agent/{agent_id}")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Agent移除成功: {data['message']}")
                return True
            else:
                print(f"❌ Agent移除失败: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Agent移除异常: {e}")
            return False
    
    def run_full_test(self):
        """运行完整测试流程"""
        print("🚀 开始运行Browser-Use Multi-Agent API测试")
        print("=" * 50)
        
        # 1. 健康检查
        if not self.test_health_check():
            print("❌ 健康检查失败，停止测试")
            return
        
        # 2. 测试直接运行任务（推荐用于简单测试）
        simple_task = "前往百度首页，搜索'人工智能'，获取前3个搜索结果"
        if self.test_run_task(simple_task):
            print("✅ 直接运行任务测试通过")
        else:
            print("❌ 直接运行任务测试失败")
        
        print("\n" + "=" * 50)
        
        # 3. 测试创建和管理Agent
        complex_task = "前往知乎首页，搜索'机器学习'，获取热门话题"
        agent_id = self.test_create_agent(complex_task)
        
        if agent_id:
            # 4. 列出所有Agent
            self.test_list_agents()
            
            # 5. 运行Agent
            if self.test_run_agent(agent_id):
                print("✅ Agent运行测试通过")
            else:
                print("❌ Agent运行测试失败")
            
            # 6. 移除Agent
            self.test_remove_agent(agent_id)
            
            # 7. 再次列出Agent确认移除
            self.test_list_agents()
        
        print("\n" + "=" * 50)
        print("🎉 测试完成！")

def main():
    """主函数"""
    print("Browser-Use Multi-Agent API 测试工具")
    print("请确保API服务已启动在 http://localhost:8000")
    print()
    
    # 检查服务是否可用
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ API服务连接正常")
        else:
            print("❌ API服务连接异常")
            return
    except requests.exceptions.RequestException:
        print("❌ 无法连接到API服务，请确保服务已启动")
        print("启动命令: python run_browser_use.py")
        return
    
    # 运行测试
    tester = BrowserUseAPITester()
    tester.run_full_test()

if __name__ == "__main__":
    main()
