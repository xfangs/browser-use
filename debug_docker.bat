@echo off
echo ========================================
echo Docker构建问题诊断脚本
echo ========================================
echo.

echo 1. 检查Docker版本...
docker --version
echo.

echo 2. 检查Docker状态...
docker info | findstr "Server Version"
docker info | findstr "Operating System"
echo.

echo 3. 检查可用磁盘空间...
wmic logicaldisk get size,freespace,caption
echo.

echo 4. 检查网络连接...
ping -n 1 pypi.tuna.tsinghua.edu.cn
echo.

echo 5. 清理Docker缓存...
docker system prune -f
echo.

echo 6. 尝试分步构建测试...
echo 步骤1: 基础镜像测试
docker run --rm python:3.11-slim python -c "print('基础镜像正常')"
echo.

if %ERRORLEVEL% EQU 0 (
    echo 基础镜像测试通过！
    echo.
    echo 步骤2: 尝试安装系统包
    docker run --rm python:3.11-slim bash -c "apt-get update && apt-get install -y fonts-liberation && echo '字体包安装成功'"
    echo.
    
    if %ERRORLEVEL% EQU 0 (
        echo 系统包安装测试通过！
        echo.
        echo 建议使用主版本Dockerfile重新构建
    ) else (
        echo 系统包安装失败，建议使用备用版本
    )
) else (
    echo 基础镜像测试失败，请检查Docker环境
)

echo.
echo ========================================
echo 诊断完成
echo ========================================
pause

