import requests
import json

# API基础URL
BASE_URL = "http://localhost:8000"

def test_health():
    """测试健康检查接口"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"健康检查: {response.status_code}")
        print(f"响应: {response.json()}")
        return True
    except Exception as e:
        print(f"健康检查失败: {e}")
        return False

def test_run_task_basic():
    """测试基本任务执行接口"""
    task_data = {
        "task": "访问百度首页并搜索'Python'",
        "cdp_url": "http://127.0.0.1:9222",
        "model": "qwen2.5:7b",
        "host": "http://127.0.0.1:11434",
        "max_steps": 20,  # 适中的步骤数
        "headless": False,
        "verbose": True,
        "timeout": 120,  # 2分钟超时
        "retry_count": 2,  # 重试2次
        "wait_for_completion": True
    }
    
    try:
        print("发送基本任务请求...")
        response = requests.post(
            f"{BASE_URL}/run_task",
            json=task_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"任务执行状态: {response.status_code}")
        result = response.json()
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get("success"):
            print("✅ 基本任务执行成功!")
            if "steps_executed" in result:
                print(f"执行步骤数: {result['steps_executed']}")
            if "execution_time" in result:
                print(f"执行时间: {result['execution_time']:.2f}秒")
        else:
            print("❌ 基本任务执行失败!")
            
        return result.get("success", False)
        
    except Exception as e:
        print(f"基本任务执行请求失败: {e}")
        return False

def test_run_task_complex():
    """测试复杂任务执行接口（更多步骤和更长超时）"""
    task_data = {
        "task": "访问GitHub，搜索Python项目，查看前3个项目的README内容",
        "cdp_url": "http://127.0.0.1:9222",
        "model": "qwen2.5:7b",
        "host": "http://127.0.0.1:11434",
        "max_steps": 80,  # 更多步骤
        "headless": False,
        "verbose": True,
        "timeout": 300,  # 5分钟超时
        "retry_count": 3,  # 重试3次
        "wait_for_completion": True
    }
    
    try:
        print("发送复杂任务请求...")
        response = requests.post(
            f"{BASE_URL}/run_task",
            json=task_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"复杂任务执行状态: {response.status_code}")
        result = response.json()
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get("success"):
            print("✅ 复杂任务执行成功!")
            if "steps_executed" in result:
                print(f"执行步骤数: {result['steps_executed']}")
            if "execution_time" in result:
                print(f"执行时间: {result['execution_time']:.2f}秒")
        else:
            print("❌ 复杂任务执行失败!")
            
        return result.get("success", False)
        
    except Exception as e:
        print(f"复杂任务执行请求失败: {e}")
        return False

def test_run_task_with_custom_params():
    """测试自定义参数的任务执行"""
    task_data = {
        "task": "访问Stack Overflow，搜索'Python async'相关问题",
        "cdp_url": "http://127.0.0.1:9222",
        "model": "qwen2.5:7b",
        "host": "http://127.0.0.1:11434",
        "max_steps": 60,
        "headless": True,  # 无头模式
        "verbose": False,  # 不显示详细日志
        "timeout": 180,
        "retry_count": 1,  # 只重试1次
        "wait_for_completion": False  # 不等待完成
    }
    
    try:
        print("发送自定义参数任务请求...")
        response = requests.post(
            f"{BASE_URL}/run_task",
            json=task_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"自定义参数任务执行状态: {response.status_code}")
        result = response.json()
        print(f"响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        if result.get("success"):
            print("✅ 自定义参数任务执行成功!")
        else:
            print("❌ 自定义参数任务执行失败!")
            
        return result.get("success", False)
        
    except Exception as e:
        print(f"自定义参数任务执行请求失败: {e}")
        return False

if __name__ == "__main__":
    print("=== Browser-Use 优化版API测试 ===\n")
    
    # 测试健康检查
    print("1. 测试健康检查接口")
    if not test_health():
        print("❌ 服务可能未启动，请先运行 python run_browser_use.py")
        exit(1)
    print()
    
    # 测试基本任务执行
    print("2. 测试基本任务执行接口")
    test_run_task_basic()
    print()
    
    # 测试复杂任务执行
    print("3. 测试复杂任务执行接口")
    test_run_task_complex()
    print()
    
    # 测试自定义参数任务执行
    print("4. 测试自定义参数任务执行接口")
    test_run_task_with_custom_params()
    
    print("\n=== 测试完成 ===")

