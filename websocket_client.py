#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Browser-Use Multi-Agent WebSocket 客户端测试脚本
用于实时监控Agent的推理过程
"""

import asyncio
import websockets
import json
import time
from typing import Dict, Any
import requests

class WebSocketClient:
    def __init__(self, base_url: str = "ws://localhost:8000"):
        self.base_url = base_url
        self.http_base_url = base_url.replace("ws://", "http://").replace("wss://", "https://")
        self.websocket = None
        self.agent_id = None
    
    async def connect_to_agent(self, agent_id: str):
        """连接到指定Agent的WebSocket"""
        try:
            uri = f"{self.base_url}/ws/{agent_id}"
            print(f"🔄 正在连接到: {uri}")
            
            self.websocket = await websockets.connect(uri)
            self.agent_id = agent_id
            
            print(f"✅ 已连接到Agent: {agent_id}")
            
            # 开始监听消息
            await self.listen_for_messages()
            
        except Exception as e:
            print(f"❌ 连接失败: {e}")
    
    async def listen_for_messages(self):
        """监听WebSocket消息"""
        try:
            async for message in self.websocket:
                try:
                    data = json.loads(message)
                    await self.handle_message(data)
                except json.JSONDecodeError:
                    print(f"📨 收到非JSON消息: {message}")
                    
        except websockets.exceptions.ConnectionClosed:
            print("🔌 WebSocket连接已关闭")
        except Exception as e:
            print(f"❌ 监听消息时出错: {e}")
    
    async def handle_message(self, data: Dict[str, Any]):
        """处理接收到的消息"""
        msg_type = data.get("type", "unknown")
        message = data.get("message", "")
        timestamp = data.get("timestamp", 0)
        
        # 格式化时间戳
        time_str = time.strftime("%H:%M:%S", time.localtime(timestamp))
        
        # 根据消息类型进行不同的处理
        if msg_type == "connection":
            print(f"🔗 [{time_str}] 连接状态: {message}")
        elif msg_type == "status":
            print(f"📊 [{time_str}] 状态更新: {message}")
        elif msg_type == "log":
            print(f"📝 [{time_str}] 日志: {message}")
        elif msg_type == "step":
            print(f"🚀 [{time_str}] 执行步骤: {message}")
        elif msg_type == "error":
            print(f"❌ [{time_str}] 错误: {message}")
        elif msg_type == "warning":
            print(f"⚠️ [{time_str}] 警告: {message}")
        elif msg_type == "pong":
            print(f"💓 [{time_str}] 心跳响应: {message}")
        else:
            print(f"❓ [{time_str}] 未知消息类型 {msg_type}: {message}")
    
    async def send_heartbeat(self):
        """发送心跳消息"""
        if self.websocket and self.websocket.open:
            try:
                await self.websocket.send("ping")
            except Exception as e:
                print(f"❌ 发送心跳失败: {e}")
    
    async def close(self):
        """关闭WebSocket连接"""
        if self.websocket:
            await self.websocket.close()
            print("🔌 WebSocket连接已关闭")

class AgentMonitor:
    def __init__(self, http_base_url: str = "http://localhost:8000"):
        self.http_base_url = http_base_url
        self.websocket_client = WebSocketClient()
    
    async def monitor_agent_creation_and_execution(self):
        """监控Agent创建和执行过程"""
        print("🚀 开始监控Agent创建和执行过程")
        print("=" * 60)
        
        # 1. 创建Agent
        print("📋 步骤1: 创建Agent")
        agent_id = await self.create_agent()
        if not agent_id:
            print("❌ 创建Agent失败")
            return
        
        print(f"✅ Agent创建成功: {agent_id}")
        print()
        
        # 2. 连接到WebSocket
        print("📋 步骤2: 连接WebSocket监控")
        websocket_task = asyncio.create_task(
            self.websocket_client.connect_to_agent(agent_id)
        )
        
        # 等待连接建立
        await asyncio.sleep(2)
        
        # 3. 运行Agent
        print("📋 步骤3: 运行Agent")
        await self.run_agent(agent_id)
        
        # 等待一段时间以接收所有WebSocket消息
        print("⏳ 等待推理过程完成...")
        await asyncio.sleep(10)
        
        # 4. 清理
        print("📋 步骤4: 清理Agent")
        await self.remove_agent(agent_id)
        
        # 关闭WebSocket连接
        await self.websocket_client.close()
        
        print("=" * 60)
        print("🎉 监控完成！")
    
    async def create_agent(self) -> str:
        """创建Agent"""
        try:
            payload = {
                "cdp_url": "http://127.0.0.1:9222",
                "model": "qwen2.5:7b",
                "host": "http://127.0.0.1:11434",
                "task": "前往百度首页，搜索'人工智能'，获取前3个搜索结果",
                "max_steps": 10,
                "headless": True,
                "verbose": False
            }
            
            response = requests.post(
                f"{self.http_base_url}/create_agent",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data["result"]["agent_id"]
            else:
                print(f"❌ 创建Agent失败: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 创建Agent异常: {e}")
            return None
    
    async def run_agent(self, agent_id: str):
        """运行Agent"""
        try:
            response = requests.post(
                f"{self.http_base_url}/run_agent/{agent_id}",
                timeout=300  # 5分钟超时
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Agent运行完成: {data['message']}")
            else:
                print(f"❌ Agent运行失败: {response.status_code} - {response.text}")
                
        except Exception as e:
            print(f"❌ 运行Agent异常: {e}")
    
    async def remove_agent(self, agent_id: str):
        """移除Agent"""
        try:
            response = requests.delete(
                f"{self.http_base_url}/remove_agent/{agent_id}",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Agent移除成功: {data['message']}")
            else:
                print(f"❌ Agent移除失败: {response.status_code}")
                
        except Exception as e:
            print(f"❌ 移除Agent异常: {e}")

async def main():
    """主函数"""
    print("Browser-Use Multi-Agent WebSocket 监控工具")
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
    
    # 创建监控器并开始监控
    monitor = AgentMonitor()
    await monitor.monitor_agent_creation_and_execution()

if __name__ == "__main__":
    asyncio.run(main())
