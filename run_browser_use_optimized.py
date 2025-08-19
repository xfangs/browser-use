#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
使用ChatOllama的优化版推理代码 - 解决超时问题
"""

import asyncio
import logging
import time
from browser_use import Agent, BrowserSession
from browser_use.llm import ChatOllama
from config import config

# 配置日志
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler('browser_use.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BrowserUseRunner:
    """浏览器使用运行器类"""
    
    def __init__(self):
        self.llm = None
        self.browser_session = None
        self.agent = None
        
    async def initialize_llm(self):
        """初始化ChatOllama实例"""
        print("正在初始化ChatOllama...")
        try:
            self.llm = ChatOllama(
                host=config.OLLAMA_HOST,
                model=config.OLLAMA_MODEL
            )
            print(f"✅ ChatOllama初始化成功，使用模型: {config.OLLAMA_MODEL}")
            return True
        except Exception as e:
            logger.error(f"ChatOllama初始化失败: {e}")
            return False
    
    async def initialize_browser(self):
        """初始化浏览器会话"""
        print("正在连接浏览器...")
        try:
            browser_config = config.get_browser_config()
            self.browser_session = BrowserSession(
                cdp_url=browser_config["cdp_url"],
                keep_alive=browser_config.get("keep_alive", False)
            )
            print("✅ 浏览器连接成功")
            return True
        except Exception as e:
            logger.error(f"浏览器连接失败: {e}")
            return False
    
    async def initialize_agent(self, task_name="ai_world_model_research"):
        """初始化Agent实例"""
        print("正在创建Agent...")
        try:
            task_config = config.get_task_config(task_name)
            agent_config = config.get_agent_config()
            
            # 使用配置的任务描述
            task_description = task_config["description"]
            
            self.agent = Agent(
                task=task_description,
                llm=self.llm,
                browser_session=self.browser_session,
                verbose=agent_config["verbose"],
                max_steps=agent_config["max_steps"],
                timeout=agent_config["timeout"],
                memory=agent_config["memory"]
            )
            print(f"✅ Agent创建成功，任务: {task_config['title']}")
            return True
        except Exception as e:
            logger.error(f"Agent创建失败: {e}")
            return False
    
    async def run_task(self):
        """执行任务"""
        print("开始执行任务...")
        start_time = time.time()
        
        try:
            # 设置更长的超时时间
            result = await asyncio.wait_for(
                self.agent.run(),
                timeout=config.AGENT_TIMEOUT * 2  # 双倍超时时间
            )
            
            execution_time = time.time() - start_time
            print(f"✅ 任务执行完成！耗时: {execution_time:.2f}秒")
            
            # 分析结果
            await self.analyze_results(result)
            return result
            
        except asyncio.TimeoutError:
            logger.error(f"任务执行超时 (>{config.AGENT_TIMEOUT * 2}秒)")
            print("❌ 任务执行超时，请检查网络连接或增加超时时间")
            return None
        except Exception as e:
            logger.error(f"任务执行失败: {e}")
            print(f"❌ 详细错误信息: {type(e).__name__}: {e}")
            return None
    
    async def analyze_results(self, result):
        """分析任务执行结果"""
        if not result:
            print("❌ 没有可分析的结果")
            return
        
        try:
            if hasattr(result, 'all_results') and result.all_results:
                success_count = sum(1 for r in result.all_results if r.success)
                total_count = len(result.all_results)
                
                print(f"\n📊 执行结果统计:")
                print(f"   总步骤数: {total_count}")
                print(f"   成功步骤: {success_count}")
                print(f"   失败步骤: {total_count - success_count}")
                print(f"   成功率: {(success_count/total_count)*100:.1f}%")
                
                # 显示详细结果
                print(f"\n📋 详细执行记录:")
                for i, action_result in enumerate(result.all_results):
                    status = "✅" if action_result.success else "❌"
                    print(f"   步骤 {i+1}: {status}")
                    
                    if action_result.error:
                        print(f"     错误: {action_result.error}")
                    if action_result.extracted_content:
                        content = str(action_result.extracted_content)[:100]
                        print(f"     内容: {content}...")
                        
        except Exception as e:
            logger.error(f"结果分析失败: {e}")
    
    async def cleanup(self):
        """清理资源"""
        print("正在清理资源...")
        try:
            if self.browser_session:
                await self.browser_session.close()
                print("✅ 浏览器会话已关闭")
        except Exception as e:
            logger.error(f"清理资源时出错: {e}")
    
    async def run(self, task_name="ai_world_model_research"):
        """运行完整的任务流程"""
        try:
            # 1. 初始化LLM
            if not await self.initialize_llm():
                return False
            
            # 2. 初始化浏览器
            if not await self.initialize_browser():
                return False
            
            # 3. 初始化Agent
            if not await self.initialize_agent(task_name):
                return False
            
            # 4. 执行任务
            result = await self.run_task()
            
            return result is not None
            
        except Exception as e:
            logger.error(f"运行过程中发生错误: {e}")
            return False
        finally:
            await self.cleanup()

async def main():
    """主函数"""
    print("🚀 启动优化版Browser Use程序")
    print("=" * 50)
    
    # 创建运行器实例
    runner = BrowserUseRunner()
    
    # 运行任务
    success = await runner.run()
    
    if success:
        print("\n🎉 程序执行成功完成！")
    else:
        print("\n💥 程序执行失败，请检查日志文件获取详细信息")
    
    print("=" * 50)

def check_prerequisites():
    """检查运行前提条件"""
    print("🔍 检查运行环境...")
    
    # 检查Ollama服务
    try:
        import requests
        response = requests.get(f"{config.OLLAMA_HOST}/api/tags", timeout=config.REQUEST_TIMEOUT)
        if response.status_code == 200:
            print("✅ Ollama服务运行正常")
        else:
            print("❌ Ollama服务响应异常")
            return False
    except Exception as e:
        print(f"❌ 无法连接到Ollama服务: {e}")
        print(f"请确保Ollama服务已启动: ollama serve")
        return False
    
    # 检查Chrome调试端口
    try:
        response = requests.get(f"{config.CHROME_CDP_URL}/json/version", timeout=config.REQUEST_TIMEOUT)
        if response.status_code == 200:
            print("✅ Chrome调试端口可用")
        else:
            print("❌ Chrome调试端口响应异常")
            return False
    except Exception as e:
        print(f"❌ 无法连接到Chrome调试端口: {e}")
        print(f"请确保Chrome以调试模式启动: chrome --remote-debugging-port={config.CHROME_DEBUG_PORT}")
        return False
    
    print("✅ 环境检查通过")
    return True

if __name__ == "__main__":
    # 检查前提条件
    if not check_prerequisites():
        print("❌ 环境检查失败，请解决上述问题后重试")
        exit(1)
    
    # 运行异步主函数
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️ 程序被用户中断")
    except Exception as e:
        logger.error(f"程序运行异常: {e}")
        print(f"💥 程序异常退出: {e}")
