# Docker 构建问题修复说明

## 问题描述

原始 Docker 构建失败，错误信息显示：

```
Package 'ttf-unifont' has no installation candidate
Package 'ttf-ubuntu-font-family' has no installation candidate
```

这是因为在 Debian 12 (trixie) 中，某些字体包名已经改变。

## 修复方案（三层架构）

### 1. 主修复版本 (Dockerfile)

- 分步安装系统依赖，避免一次性安装过多包
- 使用兼容的字体包：`fonts-liberation`, `fonts-noto-color-emoji`
- 添加错误处理的 Playwright 安装流程
- 适合大多数环境

### 2. 备用版本 (Dockerfile.backup)

- 使用最小依赖配置
- 跳过 Playwright 依赖检查：`--with-deps=false`
- 适合依赖安装有问题的环境

### 3. 超简化版本 (Dockerfile.minimal)

- 最简配置，仅安装基础工具
- 跳过复杂的系统依赖
- 用于快速测试和调试

## 使用方法

### 方法 1：使用智能构建脚本（推荐）

```bash
# Windows CMD
build_docker.bat

# Windows PowerShell
.\build_docker.ps1
```

脚本会自动尝试三个版本，直到成功为止。

### 方法 2：手动构建

```bash
# 主版本
docker build -t runbrowseruse:latest .

# 备用版本
docker build -f Dockerfile.backup -t runbrowseruse:backup .

# 超简化版本
docker build -f Dockerfile.minimal -t runbrowseruse:minimal .
```

### 方法 3：运行容器

```bash
# 使用主版本
docker run -p 8080:8080 runbrowseruse:latest

# 使用备用版本
docker run -p 8080:8080 runbrowseruse:backup

# 使用超简化版本
docker run -p 8080:8080 runbrowseruse:minimal
```

## 调试工具

### 诊断脚本

```bash
# Windows CMD
debug_docker.bat
```

诊断脚本会检查：

- Docker 版本和状态
- 磁盘空间
- 网络连接
- 基础镜像测试
- 系统包安装测试

## 修复的关键点

1. **分步安装**：避免一次性安装过多包导致的失败
2. **字体包兼容性**：使用 Debian 12 兼容的字体包名
3. **错误处理**：Playwright 安装失败时继续构建
4. **三层架构**：提供多个备选方案
5. **智能构建**：自动尝试不同版本直到成功

## 测试建议

1. 先运行诊断脚本：`debug_docker.bat`
2. 使用智能构建脚本：`build_docker.bat`
3. 如果自动构建失败，手动尝试不同版本
4. 构建成功后测试容器运行
5. 验证 Playwright 功能是否正常

## 常见问题解决

### 问题 1：系统包安装失败

- 使用备用版本：`Dockerfile.backup`
- 检查网络连接和镜像源

### 问题 2：Playwright 安装失败

- 使用超简化版本：`Dockerfile.minimal`
- 检查 Python 依赖是否正确安装

### 问题 3：构建过程卡住

- 清理 Docker 缓存：`docker system prune -a`
- 检查磁盘空间是否充足

## 注意事项

- 确保 Docker Desktop 正在运行
- 构建过程可能需要几分钟时间
- 如果所有版本都失败，检查 Docker 环境配置
- 建议定期清理 Docker 缓存和镜像
