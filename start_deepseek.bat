@echo off
chcp 65001 >nul
echo 🚀 DeepSeek LLM 浏览器自动化启动脚本
echo ==========================================

REM 检查是否设置了API密钥
if "%DEEPSEEK_API_KEY%"=="" (
    echo ❌ 未设置DeepSeek API密钥
    echo.
    echo 请按以下步骤操作：
    echo 1. 访问 https://platform.deepseek.com/ 获取API密钥
    echo 2. 设置环境变量: set DEEPSEEK_API_KEY=your-api-key
    echo 3. 或者创建.env文件并设置API密钥
    echo.
    pause
    exit /b 1
)

echo ✅ DeepSeek API密钥已配置
echo.

REM 检查Chrome调试端口
echo 🔍 检查Chrome调试端口...
powershell -Command "try { $response = Invoke-WebRequest -Uri 'http://127.0.0.1:9222/json/version' -TimeoutSec 5; if ($response.StatusCode -eq 200) { Write-Host '✅ Chrome调试端口可用' } else { Write-Host '❌ Chrome调试端口响应异常' } } catch { Write-Host '❌ 无法连接到Chrome调试端口' }"

echo.
echo 📋 启动要求：
echo 1. ✅ DeepSeek API密钥已配置
echo 2. ⚠️  请确保Chrome以调试模式启动: chrome --remote-debugging-port=9222
echo 3. ⚠️  请确保网络连接正常
echo.

echo 🚀 正在启动程序...
python run_browser_use.py

echo.
echo 程序已退出
pause
