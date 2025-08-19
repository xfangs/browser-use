import requests
import time
import json
from typing import Dict, Any

class AsyncBrowserUseAPITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def test_async_task_execution(self, task: str) -> bool:
        """测试异步任务执行"""
        try:
            print(f"🔄 提交异步任务: {task[:50]}...")
            
            # 提交任务
            payload = {
                "cdp_url": "http://127.0.0.1:9222",
                "model": "qwen2.5:7b",
                "host": "http://127.0.0.1:11434",
                "task": task,
                "max_steps": 5,
                "headless": True,
                "verbose": False,
                "timeout": 300
            }
            
            response = self.session.post(f"{self.base_url}/run_task", json=payload)
            if response.status_code != 200:
                print(f"❌ 提交任务失败: {response.status_code} - {response.text}")
                return False
            
            data = response.json()
            task_id = data.get("task_id")
            if not task_id:
                print(f"❌ 未获取到任务ID: {data}")
                return False
            
            print(f"✅ 任务提交成功，任务ID: {task_id}")
            
            # 监控任务状态
            return self.monitor_task_status(task_id)
            
        except Exception as e:
            print(f"❌ 测试异步任务执行异常: {e}")
            return False
    
    def monitor_task_status(self, task_id: str) -> bool:
        """监控任务状态"""
        print(f"📊 开始监控任务 {task_id} 的状态...")
        
        max_wait_time = 300  # 最大等待5分钟
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            try:
                # 获取任务状态
                response = self.session.get(f"{self.base_url}/task_status/{task_id}")
                if response.status_code != 200:
                    print(f"❌ 获取任务状态失败: {response.status_code}")
                    time.sleep(2)
                    continue
                
                status_data = response.json()
                status = status_data.get("status")
                message = status_data.get("message", "")
                progress = status_data.get("progress", 0.0)
                
                print(f"📈 任务状态: {status} | 进度: {progress:.1%} | 消息: {message}")
                
                if status == "completed":
                    result = status_data.get("result")
                    execution_time = status_data.get("end_time", 0) - status_data.get("start_time", 0)
                    print(f"✅ 任务执行完成！耗时: {execution_time:.2f}秒")
                    if result:
                        print(f"📋 执行结果: {result}")
                    return True
                
                elif status == "failed":
                    error = status_data.get("error", "未知错误")
                    print(f"❌ 任务执行失败: {error}")
                    return False
                
                elif status in ["pending", "running"]:
                    time.sleep(2)  # 等待2秒后再次检查
                    continue
                
                else:
                    print(f"⚠️ 未知任务状态: {status}")
                    time.sleep(2)
                    continue
                    
            except Exception as e:
                print(f"❌ 监控任务状态异常: {e}")
                time.sleep(2)
                continue
        
        print(f"⏰ 任务监控超时（{max_wait_time}秒）")
        return False
    
    def test_list_tasks(self) -> bool:
        """测试列出所有任务"""
        try:
            print("📋 获取任务列表...")
            response = self.session.get(f"{self.base_url}/list_tasks")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 任务列表获取成功")
                print(f"📊 总任务数: {data.get('total', 0)}")
                print(f"📈 状态统计: {json.dumps(data.get('status_summary', {}), indent=2, ensure_ascii=False)}")
                return True
            else:
                print(f"❌ 获取任务列表失败: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 测试获取任务列表异常: {e}")
            return False
    
    def test_clear_completed_tasks(self) -> bool:
        """测试清理已完成的任务"""
        try:
            print("🧹 清理已完成的任务...")
            response = self.session.delete(f"{self.base_url}/clear_completed_tasks")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 清理任务成功: {data.get('message', '')}")
                return True
            else:
                print(f"❌ 清理任务失败: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            print(f"❌ 测试清理任务异常: {e}")
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("🚀 开始运行异步推理API测试...")
        print("=" * 60)
        
        # 测试1: 异步任务执行
        print("\n🧪 测试1: 异步任务执行")
        test_task = "前往百度首页，搜索'人工智能'，获取页面标题"
        success1 = self.test_async_task_execution(test_task)
        
        # 测试2: 获取任务列表
        print("\n🧪 测试2: 获取任务列表")
        success2 = self.test_list_tasks()
        
        # 测试3: 清理已完成的任务
        print("\n🧪 测试3: 清理已完成的任务")
        success3 = self.test_clear_completed_tasks()
        
        # 测试结果汇总
        print("\n" + "=" * 60)
        print("📊 测试结果汇总:")
        print(f"✅ 异步任务执行: {'通过' if success1 else '失败'}")
        print(f"✅ 获取任务列表: {'通过' if success2 else '通过'}")
        print(f"✅ 清理已完成任务: {'通过' if success3 else '失败'}")
        
        overall_success = success1 and success2 and success3
        print(f"\n🎯 总体测试结果: {'全部通过' if overall_success else '部分失败'}")
        
        return overall_success

if __name__ == "__main__":
    tester = AsyncBrowserUseAPITester()
    tester.run_all_tests()
