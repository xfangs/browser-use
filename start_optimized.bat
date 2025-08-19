@echo off
chcp 65001 >nul
echo 🚀 启动优化版Browser_use程序
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 🔍 检查依赖包...
python -c "import browser_use" >nul 2>&1
if errorlevel 1 (
    echo ❌ 缺少browser_use包，正在安装...
    pip install browser-use
)

python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo ❌ 缺少requests包，正在安装...
    pip install requests
)

echo ✅ 依赖检查完成
echo.

REM 启动程序
echo 🚀 启动程序...
python run_browser_use_optimized.py

echo.
echo 程序执行完成
pause



