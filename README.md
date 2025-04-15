# Mini Cloud Service Platform

一个基于 Lima 和本地 Lambda 实现的迷你云服务平台，提供类似 AWS EC2 和 Lambda 的功能。

A mini cloud service platform based on Lima and local Lambda implementation, providing similar functionality to AWS EC2 and Lambda.

## 系统要求 / System Requirements

- macOS (推荐 / Recommended)
- Python 3.9+
- Homebrew
- 至少 8GB 内存 / At least 8GB RAM
- 至少 20GB 可用磁盘空间 / At least 20GB free disk space

## 安装步骤 / Installation Steps

### 1. 安装基础依赖 / Install Basic Dependencies

```bash
# 安装 Lima 和 nerdctl
brew install lima nerdctl

# 安装 Multipass (用于模拟 EC2)
brew install multipass

# 创建并激活 Python 虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
.\venv\Scripts\activate  # Windows

# 安装 Poetry
pip install poetry

# 安装项目依赖
poetry install
```

### 2. 初始化 Lima / Initialize Lima

```bash
# 启动默认 Lima 实例
limactl start default

# 验证 Lima 安装
limactl list

# 检查 Lima 状态
limactl status default
```

### 3. 配置环境变量 / Configure Environment Variables

创建 `.env` 文件并添加以下配置：

```bash
# EC2 服务配置
DEFAULT_IMAGE_URL=https://cloud-images.ubuntu.com/releases/22.04/release/ubuntu-22.04-server-cloudimg-amd64.img
DEFAULT_CPU=2
DEFAULT_MEMORY=4
DEFAULT_DISK=20

# Lambda 服务配置
LAMBDA_FUNCTIONS_DIR=~/.lambda-functions
LAMBDA_TIMEOUT=30
LAMBDA_MEMORY_LIMIT=128

# 服务端口配置
EC2_SERVICE_PORT=8000
LAMBDA_SERVICE_PORT=8001
```

## 启动服务 / Start Services

### 1. 启动 EC2 服务 / Start EC2 Service

```bash
# 在第一个终端窗口
poetry run uvicorn src.ec2_service.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. 启动 Lambda 服务 / Start Lambda Service

```bash
# 在第二个终端窗口
poetry run uvicorn src.lambda_service.main:app --host 0.0.0.0 --port 8001 --reload
```

## 使用指南 / Usage Guide

### EC2 服务 / EC2 Service

#### 创建虚拟机 / Create VM

```bash
curl -X POST "http://localhost:8000/instances" \
     -H "Content-Type: application/json" \
     -d '{
           "name": "my-vm",
           "image_url": "https://cloud-images.ubuntu.com/releases/22.04/release/ubuntu-22.04-server-cloudimg-amd64.img",
           "cpu": 2,
           "memory": 4,
           "disk": 20
         }'
```

#### 查看虚拟机状态 / Check VM Status

```bash
curl "http://localhost:8000/instances/my-vm"
```

#### 启动/停止虚拟机 / Start/Stop VM

```bash
# 启动
curl -X POST "http://localhost:8000/instances/my-vm/actions" \
     -H "Content-Type: application/json" \
     -d '{"action": "start"}'

# 停止
curl -X POST "http://localhost:8000/instances/my-vm/actions" \
     -H "Content-Type: application/json" \
     -d '{"action": "stop"}'
```

#### 删除虚拟机 / Delete VM

```bash
curl -X DELETE "http://localhost:8000/instances/my-vm"
```

#### 查看虚拟机列表 / List VMs

```bash
curl "http://localhost:8000/instances"
```

### Lambda 服务 / Lambda Service

#### 部署函数 / Deploy Function

```bash
curl -X POST "http://localhost:8001/functions/hello-world" \
     -F "code=@lambda_function.py"
```

示例函数文件 `lambda_function.py`:

```python
def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": {
            "message": "Hello from Lambda!"
        }
    }
```

#### 调用函数 / Invoke Function

```bash
curl -X POST "http://localhost:8001/2015-03-31/functions/hello-world/invocations" \
     -H "Content-Type: application/json" \
     -d '{"name": "World"}'
```

#### 查看函数列表 / List Functions

```bash
curl "http://localhost:8001/functions"
```

#### 删除函数 / Delete Function

```bash
curl -X DELETE "http://localhost:8001/functions/hello-world"
```

## 常见问题 / FAQ

### 1. Lima 实例无法启动 / Lima Instance Fails to Start

检查 Lima 日志：
```bash
limactl logs default
```

检查 Lima 配置：
```bash
limactl show default
```

### 2. 虚拟机 SSH 连接问题 / VM SSH Connection Issues

获取 SSH 端口：
```bash
limactl list --json
```

使用 SSH 连接：
```bash
ssh -p <port> lima@localhost
```

### 3. Lambda 函数执行超时 / Lambda Function Timeout

检查函数执行时间，确保不超过配置的超时时间（默认 30 秒）。

### 4. 服务无法启动 / Service Fails to Start

检查端口占用：
```bash
lsof -i :8000
lsof -i :8001
```

检查日志：
```bash
# EC2 服务日志
poetry run uvicorn src.ec2_service.main:app --host 0.0.0.0 --port 8000 --log-level debug

# Lambda 服务日志
poetry run uvicorn src.lambda_service.main:app --host 0.0.0.0 --port 8001 --log-level debug
```

## 开发指南 / Development Guide

### 项目结构 / Project Structure

```
.
├── src/
│   ├── ec2_service/     # EC2 服务实现
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── config.py
│   │   └── lima_vm.py
│   └── lambda_service/  # Lambda 服务实现
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       ├── config.py
│       └── runtime.py
├── tests/               # 测试文件
├── .env                 # 环境变量配置
└── pyproject.toml       # 项目依赖配置
```

### 添加新功能 / Adding New Features

1. 创建新的分支
2. 实现功能
3. 添加测试
4. 提交 Pull Request

### 运行测试 / Running Tests

```bash
# 运行所有测试
poetry run pytest

# 运行特定测试
poetry run pytest tests/ec2_service/test_vm.py
```

### 代码格式化 / Code Formatting

```bash
# 格式化代码
poetry run black src tests

# 排序导入
poetry run isort src tests

# 检查代码质量
poetry run flake8 src tests
```

## 许可证 / License

MIT License