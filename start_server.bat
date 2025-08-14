@echo off
echo 启动 Browser-Use Multi-Agent HTTP API 服务...
echo.
echo 请确保以下服务已启动：
echo 1. Chrome浏览器（开启远程调试模式）
echo 2. Ollama服务
echo.
echo 服务将在 http://localhost:8000 启动
echo API文档地址: http://localhost:8000/docs
echo.
pause
python run_browser_use.py
pause
