# DeepSeek LLM 浏览器自动化启动脚本
Write-Host "🚀 DeepSeek LLM 浏览器自动化启动脚本" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 检查是否设置了API密钥
if (-not $env:DEEPSEEK_API_KEY -or $env:DEEPSEEK_API_KEY -eq "your-deepseek-api-key-here") {
    Write-Host "❌ 未设置DeepSeek API密钥" -ForegroundColor Red
    Write-Host ""
    Write-Host "请按以下步骤操作：" -ForegroundColor Yellow
    Write-Host "1. 访问 https://platform.deepseek.com/ 获取API密钥" -ForegroundColor White
    Write-Host "2. 设置环境变量: `$env:DEEPSEEK_API_KEY='your-api-key'" -ForegroundColor White
    Write-Host "3. 或者创建.env文件并设置API密钥" -ForegroundColor White
    Write-Host ""
    Read-Host "按回车键退出"
    exit 1
}

Write-Host "✅ DeepSeek API密钥已配置" -ForegroundColor Green
Write-Host ""

# 检查Chrome调试端口
Write-Host "🔍 检查Chrome调试端口..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:9222/json/version" -TimeoutSec 5
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ Chrome调试端口可用" -ForegroundColor Green
    } else {
        Write-Host "❌ Chrome调试端口响应异常" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ 无法连接到Chrome调试端口" -ForegroundColor Red
    Write-Host "请确保Chrome以调试模式启动: chrome --remote-debugging-port=9222" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "📋 启动要求：" -ForegroundColor Cyan
Write-Host "1. ✅ DeepSeek API密钥已配置" -ForegroundColor Green
Write-Host "2. ⚠️  请确保Chrome以调试模式启动: chrome --remote-debugging-port=9222" -ForegroundColor Yellow
Write-Host "3. ⚠️  请确保网络连接正常" -ForegroundColor Yellow
Write-Host ""

Write-Host "🚀 正在启动程序..." -ForegroundColor Green
python run_browser_use.py

Write-Host ""
Write-Host "程序已退出" -ForegroundColor Cyan
Read-Host "按回车键退出"
