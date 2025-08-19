Write-Host "开始构建Docker镜像..." -ForegroundColor Green
Write-Host ""

Write-Host "清理旧的镜像..." -ForegroundColor Yellow
docker rmi runbrowseruse:latest 2>$null
docker system prune -f

Write-Host ""
Write-Host "尝试构建主版本..." -ForegroundColor Yellow
docker build -t runbrowseruse:latest .

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "主版本构建成功！镜像标签: runbrowseruse:latest" -ForegroundColor Green
    Write-Host ""
    Write-Host "运行容器测试:" -ForegroundColor Cyan
    Write-Host "docker run -p 8080:8080 runbrowseruse:latest" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "主版本构建失败！错误代码: $LASTEXITCODE" -ForegroundColor Red
    Write-Host ""
    Write-Host "尝试构建备用版本..." -ForegroundColor Yellow
    
    docker build -f Dockerfile.backup -t runbrowseruse:backup .
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "备用版本构建成功！镜像标签: runbrowseruse:backup" -ForegroundColor Green
        Write-Host ""
        Write-Host "运行容器测试:" -ForegroundColor Cyan
        Write-Host "docker run -p 8080:8080 runbrowseruse:backup" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "备用版本构建失败！错误代码: $LASTEXITCODE" -ForegroundColor Red
        Write-Host ""
        Write-Host "尝试构建超简化版本..." -ForegroundColor Yellow
        
        docker build -f Dockerfile.minimal -t runbrowseruse:minimal .
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "超简化版本构建成功！镜像标签: runbrowseruse:minimal" -ForegroundColor Green
            Write-Host ""
            Write-Host "运行容器测试:" -ForegroundColor Cyan
            Write-Host "docker run -p 8080:8080 runbrowseruse:minimal" -ForegroundColor White
        } else {
            Write-Host ""
            Write-Host "所有版本构建都失败了！错误代码: $LASTEXITCODE" -ForegroundColor Red
            Write-Host ""
            Write-Host "建议检查Docker环境和网络连接" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Read-Host "按回车键继续..."
