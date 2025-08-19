Write-Host "启动Ollama服务..." -ForegroundColor Green
Write-Host "请确保已经安装了Ollama并下载了相应的模型" -ForegroundColor Yellow
Write-Host ""

# 检查Ollama是否已安装
try {
    $ollamaVersion = ollama --version
    Write-Host "检测到Ollama版本: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "错误: 未找到Ollama，请先安装Ollama" -ForegroundColor Red
    Write-Host "下载地址: https://ollama.ai/" -ForegroundColor Cyan
    Read-Host "按回车键退出"
    exit 1
}

Write-Host "启动Ollama服务..." -ForegroundColor Green
ollama serve

Read-Host "按回车键退出"


