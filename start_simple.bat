@echo off
echo 启动 Browser-Use 简化版 API 服务...
echo.
echo 请确保已安装依赖: pip install -r requirements.txt
echo 请确保 Chrome 浏览器已启动并开启远程调试端口 9222
echo 请确保 Ollama 服务正在运行
echo.
pause
echo.
echo 正在启动服务...
python run_browser_use.py
pause

