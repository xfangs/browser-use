@echo off
echo 开始构建Docker镜像...
echo.

echo 清理旧的镜像...
docker rmi runbrowseruse:latest 2>nul
docker system prune -f

echo.
echo 尝试构建主版本...
docker build -t runbrowseruse:latest .

if %ERRORLEVEL% EQU 0 (
    echo.
    echo 主版本构建成功！镜像标签: runbrowseruse:latest
    echo.
    echo 运行容器测试:
    echo docker run -p 8080:8080 runbrowseruse:latest
    goto :end
) else (
    echo.
    echo 主版本构建失败！错误代码: %ERRORLEVEL%
    echo.
    echo 尝试构建备用版本...
    docker build -f Dockerfile.backup -t runbrowseruse:backup .
    
    if %ERRORLEVEL% EQU 0 (
        echo.
        echo 备用版本构建成功！镜像标签: runbrowseruse:backup
        echo.
        echo 运行容器测试:
        echo docker run -p 8080:8080 runbrowseruse:backup
        goto :end
    ) else (
        echo.
        echo 备用版本构建失败！错误代码: %ERRORLEVEL%
        echo.
        echo 尝试构建超简化版本...
        docker build -f Dockerfile.minimal -t runbrowseruse:minimal .
        
        if %ERRORLEVEL% EQU 0 (
            echo.
            echo 超简化版本构建成功！镜像标签: runbrowseruse:minimal
            echo.
            echo 运行容器测试:
            echo docker run -p 8080:8080 runbrowseruse:minimal
        ) else (
            echo.
            echo 所有版本构建都失败了！错误代码: %ERRORLEVEL%
            echo.
            echo 建议检查Docker环境和网络连接
        )
    )
)

:end
echo.
pause
