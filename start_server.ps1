# Browser-Use Multi-Agent HTTP API 启动脚本
Write-Host "启动 Browser-Use Multi-Agent HTTP API 服务..." -ForegroundColor Green
Write-Host ""
Write-Host "请确保以下服务已启动：" -ForegroundColor Yellow
Write-Host "1. Chrome浏览器（开启远程调试模式）" -ForegroundColor Cyan
Write-Host "2. Ollama服务" -ForegroundColor Cyan
Write-Host ""
Write-Host "服务将在 http://localhost:8000 启动" -ForegroundColor Green
Write-Host "API文档地址: http://localhost:8000/docs" -ForegroundColor Green
Write-Host ""

# 检查Python是否安装
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python版本: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到Python，请先安装Python" -ForegroundColor Red
    Read-Host "按任意键退出"
    exit 1
}

# 检查依赖是否安装
Write-Host "检查依赖..." -ForegroundColor Yellow
try {
    python -c "import fastapi, uvicorn, browser_use" 2>$null
    Write-Host "✅ 依赖检查通过" -ForegroundColor Green
} catch {
    Write-Host "❌ 依赖检查失败，正在安装..." -ForegroundColor Red
    pip install -r requirements.txt
}

Write-Host ""
Write-Host "正在启动服务..." -ForegroundColor Green
Write-Host "按 Ctrl+C 停止服务" -ForegroundColor Yellow
Write-Host ""

# 启动服务
python run_browser_use.py
