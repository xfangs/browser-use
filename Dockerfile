# 使用Python 3.11官方镜像（更稳定、更轻量）
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DEBIAN_FRONTEND=noninteractive

# 安装系统依赖（Playwright需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    wget \
    gnupg \
    ca-certificates \
    # Playwright字体依赖
    fonts-liberation \
    fonts-noto-color-emoji \
    fonts-unifont \
    # 核心系统依赖
    libnss3 \
    libnspr4 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 设置pip镜像源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/ \
    && pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 复制依赖文件
COPY requirements.txt /app/requirements.txt

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt || \
    (echo "原requirements.txt安装失败，使用备用方案..." && \
    pip install --no-cache-dir \
    browser-use==0.5.11 \
    fastapi==0.115.6 \
    uvicorn[standard]==0.32.1 \
    pydantic==2.11.7 \
    python-dotenv==1.0.1 \
    aiohttp==3.10.5 \
    requests==2.32.3 \
    playwright==1.54.0 \
    typing-extensions==4.14.1 \
    websockets==13.0)

# 安装Playwright依赖和浏览器
RUN playwright install-deps && \
    playwright install chromium || \
    (echo "使用兼容模式安装Playwright..." && \
    playwright install chromium)

# 复制应用代码
COPY run_browser_use.py /app/run_browser_use.py

# 暴露端口
EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health', timeout=5)" || exit 1

# 运行应用
CMD ["python", "run_browser_use.py"]