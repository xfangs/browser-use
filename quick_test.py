#!/usr/bin/env python3
"""
Browser-Use 快速测试脚本
用于验证优化后的系统是否正常工作
"""

import requests
import json
import time
import sys

def test_health():
    """测试服务健康状态"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 服务健康检查通过")
            print(f"   状态: {data.get('status')}")
            print(f"   活跃会话: {data.get('active_sessions', 0)}")
            print(f"   活跃LLM: {data.get('active_llms', 0)}")
            return True
        else:
            print(f"❌ 服务健康检查失败: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ 无法连接到服务: {e}")
        return False

def test_simple_task():
    """测试简单任务"""
    print("\n🔍 测试简单任务...")
    
    task_data = {
        "task": "访问百度首页",
        "max_steps": 30,
        "timeout": 120,
        "retry_count": 2,
        "wait_for_completion": True,
        "verbose": True
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/run_task",
            json=task_data,
            headers={"Content-Type": "application/json"},
            timeout=150  # 比任务超时稍长
        )
        
        if response.status_code == 200:
            result = response.json()
            execution_time = time.time() - start_time
            
            if result.get("success"):
                print(f"✅ 简单任务执行成功!")
                print(f"   执行时间: {result.get('execution_time', 0):.2f}秒")
                print(f"   执行步骤: {result.get('steps_executed', 0)}")
                print(f"   总耗时: {execution_time:.2f}秒")
                return True
            else:
                print(f"❌ 简单任务执行失败: {result.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ 请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 简单任务测试异常: {e}")
        return False

def test_complex_task():
    """测试复杂任务"""
    print("\n🔍 测试复杂任务...")
    
    task_data = {
        "task": "访问百度首页，搜索'Python教程'，查看前3个搜索结果",
        "max_steps": 80,
        "timeout": 300,
        "retry_count": 3,
        "wait_for_completion": True,
        "verbose": True
    }
    
    try:
        start_time = time.time()
        response = requests.post(
            "http://localhost:8000/run_task",
            json=task_data,
            headers={"Content-Type": "application/json"},
            timeout=350  # 比任务超时稍长
        )
        
        if response.status_code == 200:
            result = response.json()
            execution_time = time.time() - start_time
            
            if result.get("success"):
                print(f"✅ 复杂任务执行成功!")
                print(f"   执行时间: {result.get('execution_time', 0):.2f}秒")
                print(f"   执行步骤: {result.get('steps_executed', 0)}")
                print(f"   总耗时: {execution_time:.2f}秒")
                
                # 检查结果内容
                result_text = str(result.get('result', ''))
                if len(result_text) > 100:
                    print(f"   结果长度: {len(result_text)} 字符")
                    print(f"   结果预览: {result_text[:100]}...")
                else:
                    print(f"   结果: {result_text}")
                
                return True
            else:
                print(f"❌ 复杂任务执行失败: {result.get('error', '未知错误')}")
                return False
        else:
            print(f"❌ 请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 复杂任务测试异常: {e}")
        return False

def test_configuration():
    """测试配置系统"""
    print("\n🔍 测试配置系统...")
    
    try:
        # 导入配置模块
        from config import config, get_optimized_config
        
        # 测试基本配置
        basic_config = config.get_config()
        print(f"✅ 基本配置加载成功")
        print(f"   最大步骤数: {basic_config.get('max_steps')}")
        print(f"   超时时间: {basic_config.get('timeout')}秒")
        print(f"   重试次数: {basic_config.get('retry_count')}")
        
        # 测试任务类型配置
        task_types = ["simple", "complex", "research", "quick"]
        for task_type in task_types:
            task_config = config.get_task_config(task_type)
            print(f"   {task_type}: {task_config.get('max_steps')}步, {task_config.get('timeout')}秒")
        
        # 测试优化配置
        test_tasks = [
            "搜索Python教程",
            "提取网站数据",
            "填写表单信息"
        ]
        
        print(f"\n   智能配置优化:")
        for task in test_tasks:
            optimized = get_optimized_config(task, "default")
            print(f"   '{task}': {optimized.get('max_steps')}步, {optimized.get('timeout')}秒")
        
        return True
        
    except Exception as e:
        print(f"❌ 配置系统测试失败: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("🚀 开始 Browser-Use 系统测试...")
    print("=" * 50)
    
    tests = [
        ("健康检查", test_health),
        ("配置系统", test_configuration),
        ("简单任务", test_simple_task),
        ("复杂任务", test_complex_task),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            results.append((test_name, False))
    
    # 显示测试结果摘要
    print("\n" + "=" * 50)
    print("📊 测试结果摘要:")
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n   总计: {passed}/{total} 测试通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统运行正常。")
        return True
    else:
        print("⚠️  部分测试失败，请检查系统配置。")
        return False

if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 测试过程中发生未预期的错误: {e}")
        sys.exit(1)
