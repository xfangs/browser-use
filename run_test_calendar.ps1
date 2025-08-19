Write-Host "正在运行测试代码..." -ForegroundColor Green
Write-Host "请确保已安装所有依赖包" -ForegroundColor Yellow
Write-Host ""

try {
    python test_calendar.py
} catch {
    Write-Host "运行出错: $_" -ForegroundColor Red
}

Write-Host "按任意键继续..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
