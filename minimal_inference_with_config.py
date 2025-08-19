#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用ChatOllama的最小化推理代码（带配置文件）
"""

import sys
import time
from browser_use import Agent, BrowserSession
from browser_use.llm import ChatOllama
from config import OLLAMA_CONFIG, BROWSER_CONFIG, AGENT_CONFIG, TASK_CONFIG

class MinimalInference:
    """最小化推理类"""
    
    def __init__(self, task=None, model=None, host=None):
        """
        初始化推理实例
        
        Args:
            task: 任务描述，如果为None则使用默认任务
            model: 模型名称，如果为None则使用默认模型
            host: Ollama服务地址，如果为None则使用默认地址
        """
        self.task = task or TASK_CONFIG["default_task"]
        self.model = model or OLLAMA_CONFIG["model"]
        self.host = host or OLLAMA_CONFIG["host"]
        
        self.llm = None
        self.browser_session = None
        self.agent = None
        
    def initialize_components(self):
        """初始化所有组件"""
        print("🚀 正在初始化推理组件...")
        
        # 1. 初始化ChatOllama
        print(f"  📝 初始化LLM: {self.model}")
        try:
            self.llm = ChatOllama(
                host=self.host,
                model=self.model
            )
            print("  ✅ LLM初始化成功")
        except Exception as e:
            print(f"  ❌ LLM初始化失败: {e}")
            raise
        
        # 2. 连接浏览器
        print(f"  🌐 连接浏览器: {BROWSER_CONFIG['cdp_url']}")
        try:
            self.browser_session = BrowserSession(
                cdp_url=BROWSER_CONFIG["cdp_url"]
            )
            print("  ✅ 浏览器连接成功")
        except Exception as e:
            print(f"  ❌ 浏览器连接失败: {e}")
            raise
        
        # 3. 创建Agent
        print("  🤖 创建Agent...")
        try:
            self.agent = Agent(
                task=self.task,
                llm=self.llm,
                browser_session=self.browser_session,
                verbose=AGENT_CONFIG["verbose"],
                max_steps=AGENT_CONFIG["max_steps"]
            )
            print("  ✅ Agent创建成功")
        except Exception as e:
            print(f"  ❌ Agent创建失败: {e}")
            raise
        
        print("🎉 所有组件初始化完成！")
    
    def run_inference(self):
        """运行推理"""
        if not all([self.llm, self.browser_session, self.agent]):
            raise RuntimeError("组件未完全初始化，请先调用 initialize_components()")
        
        print(f"\n🎯 开始执行任务: {self.task}")
        print(f"⏱️  最大步数: {AGENT_CONFIG['max_steps']}")
        print(f"🔍 详细模式: {'开启' if AGENT_CONFIG['verbose'] else '关闭'}")
        
        start_time = time.time()
        
        try:
            # 执行任务
            result = self.agent.run()
            
            execution_time = time.time() - start_time
            print(f"\n✅ 任务执行完成！")
            print(f"⏱️  执行时间: {execution_time:.2f}秒")
            print(f"📊 执行结果: {result}")
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            print(f"\n❌ 任务执行失败！")
            print(f"⏱️  执行时间: {execution_time:.2f}秒")
            print(f"🚨 错误信息: {e}")
            raise
    
    def cleanup(self):
        """清理资源"""
        print("\n🧹 正在清理资源...")
        
        if self.browser_session:
            try:
                self.browser_session.close()
                print("  ✅ 浏览器会话已关闭")
            except Exception as e:
                print(f"  ⚠️  关闭浏览器会话时出现警告: {e}")
        
        print("🎉 资源清理完成！")
    
    def run(self):
        """完整的推理流程"""
        try:
            self.initialize_components()
            result = self.run_inference()
            return result
        finally:
            self.cleanup()

def main():
    """主函数"""
    print("=" * 60)
    print("🤖 ChatOllama 最小化推理演示")
    print("=" * 60)
    
    # 创建推理实例
    inference = MinimalInference(
        task="访问百度首页并搜索'ChatGPT'，然后截图保存"
    )
    
    try:
        # 运行推理
        result = inference.run()
        print(f"\n🎊 推理完成！最终结果: {result}")
        
    except Exception as e:
        print(f"\n💥 推理过程中出现错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
