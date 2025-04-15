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
# 使用 curl 部署函数
curl -X POST "http://localhost:8001/functions" \
     -F "name=hello-world" \
     -F "runtime=python3.9" \
     -F "handler=lambda_handler" \
     -F "code=@lambda_function.py" \
     -F "memory=128" \
     -F "timeout=30"

# 使用 Python 部署函数
import requests

url = "http://localhost:8001/functions"
files = {
    'code': ('lambda_function.py', open('lambda_function.py', 'rb'))
}
data = {
    'name': 'hello-world',
    'runtime': 'python3.9',
    'handler': 'lambda_handler',
    'memory': '128',
    'timeout': '30'
}

response = requests.post(url, files=files, data=data)
print(response.status_code)
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
# 使用 curl 调用函数
curl -X POST "http://localhost:8001/functions/hello-world/invoke"

# 使用 Python 调用函数
import requests

url = "http://localhost:8001/functions/hello-world/invoke"
response = requests.post(url)
print(response.json())
```

#### 查看函数列表 / List Functions

```bash
# 使用 curl 查看函数列表
curl "http://localhost:8001/functions"

# 使用 Python 查看函数列表
import requests

url = "http://localhost:8001/functions"
response = requests.get(url)
print(response.json())
```

#### 删除函数 / Delete Function

```bash
# 使用 curl 删除函数
curl -X DELETE "http://localhost:8001/functions/hello-world"

# 使用 Python 删除函数
import requests

url = "http://localhost:8001/functions/hello-world"
response = requests.delete(url)
print(response.status_code)
```

#### 函数配置说明 / Function Configuration

1. 函数名称 (name)
   - 必填项
   - 只能包含字母、数字、连字符和下划线
   - 长度限制：3-64 个字符

2. 运行时 (runtime)
   - 必填项
   - 支持的运行时：
     - python3.9
     - nodejs14.x
     - java11

3. 处理函数 (handler)
   - 必填项
   - 格式：`文件名.函数名`
   - 示例：`lambda_function.lambda_handler`

4. 内存限制 (memory)
   - 可选，默认值：128MB
   - 范围：128-1024MB
   - 以 64MB 为增量

5. 超时时间 (timeout)
   - 可选，默认值：30秒
   - 范围：1-300秒

#### 函数执行环境 / Function Execution Environment

1. 临时存储
   - 每个函数执行时创建临时目录
   - 执行完成后自动清理
   - 最大可用空间：512MB

2. 环境变量
   - 支持自定义环境变量
   - 通过配置文件设置
   - 示例：
     ```bash
     LAMBDA_ENV_VAR1=value1
     LAMBDA_ENV_VAR2=value2
     ```

3. 日志记录
   - 自动记录函数执行日志
   - 包含执行时间、内存使用、返回值等信息
   - 日志文件位置：`~/.lambda-functions/logs/`

#### 错误处理 / Error Handling

1. 部署错误
   - 函数名称已存在
   - 运行时不支持
   - 代码格式错误
   - 内存配置无效

2. 执行错误
   - 函数超时
   - 内存不足
   - 运行时错误
   - 权限错误

3. 错误响应格式
   ```json
   {
     "error": {
       "code": "ErrorCode",
       "message": "Error message",
       "details": {
         "field": "Additional error details"
       }
     }
   }
   ```

#### 监控和日志 / Monitoring and Logging

1. 函数执行日志
   ```bash
   # 查看函数执行日志
   cat ~/.lambda-functions/logs/hello-world.log
   ```

2. 性能监控
   - 执行时间
   - 内存使用
   - CPU 使用率
   - 调用次数

3. 资源使用统计
   ```bash
   # 查看资源使用统计
   curl "http://localhost:8001/functions/hello-world/metrics"
   ```

#### 高级功能 / Advanced Features

1. 函数版本控制
   ```bash
   # 部署新版本
   curl -X POST "http://localhost:8001/functions/hello-world/versions" \
        -F "code=@lambda_function.py" \
        -F "description=New version with bug fixes"

   # 查看版本列表
   curl "http://localhost:8001/functions/hello-world/versions"

   # 调用特定版本
   curl -X POST "http://localhost:8001/functions/hello-world/versions/1/invoke"
   ```

2. 函数别名
   ```bash
   # 创建别名
   curl -X POST "http://localhost:8001/functions/hello-world/aliases" \
        -H "Content-Type: application/json" \
        -d '{"name": "prod", "version": "1"}'

   # 使用别名调用
   curl -X POST "http://localhost:8001/functions/hello-world/aliases/prod/invoke"
   ```

3. 并发执行控制
   ```bash
   # 设置并发限制
   curl -X PUT "http://localhost:8001/functions/hello-world/concurrency" \
        -H "Content-Type: application/json" \
        -d '{"limit": 10}'
   ```

#### 最佳实践 / Best Practices

1. 函数代码优化
   - 使用适当的内存配置
   - 避免长时间运行的操作
   - 实现错误重试机制
   - 使用缓存减少重复计算

2. 安全建议
   - 使用最小权限原则
   - 定期更新依赖包
   - 避免硬编码敏感信息
   - 使用环境变量存储配置

3. 性能优化
   - 预热函数减少冷启动
   - 使用连接池管理数据库连接
   - 实现适当的超时设置
   - 监控资源使用情况

#### 开发工具 / Development Tools

1. 本地测试工具
   ```bash
   # 安装测试工具
   pip install lambda-local

   # 本地测试函数
   lambda-local -f lambda_function.py -e event.json
   ```

2. 部署工具
   ```bash
   # 使用部署脚本
   ./deploy.sh hello-world
   ```

3. 监控工具
   ```bash
   # 实时监控函数执行
   watch -n 1 "curl http://localhost:8001/functions/hello-world/metrics"
   ```

#### 故障排除 / Troubleshooting

1. 常见问题
   - 函数部署失败
     ```bash
     # 检查部署日志
     tail -f ~/.lambda-functions/logs/deploy.log
     ```
   - 执行超时
     ```bash
     # 检查执行日志
     tail -f ~/.lambda-functions/logs/hello-world.log
     ```
   - 内存不足
     ```bash
     # 检查内存使用
     curl "http://localhost:8001/functions/hello-world/metrics?type=memory"
     ```

2. 调试技巧
   - 使用日志级别控制
     ```bash
     # 设置日志级别
     curl -X PUT "http://localhost:8001/functions/hello-world/logging" \
          -H "Content-Type: application/json" \
          -d '{"level": "DEBUG"}'
     ```
   - 启用详细日志
     ```bash
     # 启用详细日志
     curl -X PUT "http://localhost:8001/functions/hello-world/logging" \
          -H "Content-Type: application/json" \
          -d '{"verbose": true}'
     ```

#### 集成指南 / Integration Guide

1. API Gateway 集成
   ```bash
   # 创建 API 网关
   curl -X POST "http://localhost:8001/apis" \
        -H "Content-Type: application/json" \
        -d '{
          "name": "hello-api",
          "path": "/hello",
          "function": "hello-world"
        }'
   ```

2. 事件源集成
   ```bash
   # 配置定时触发器
   curl -X POST "http://localhost:8001/functions/hello-world/triggers" \
        -H "Content-Type: application/json" \
        -d '{
          "type": "schedule",
          "schedule": "rate(5 minutes)"
        }'
   ```

3. 存储服务集成
   ```bash
   # 配置存储访问
   curl -X PUT "http://localhost:8001/functions/hello-world/storage" \
        -H "Content-Type: application/json" \
        -d '{
          "type": "s3",
          "bucket": "my-bucket",
          "prefix": "data/"
        }'
   ```

#### 安全指南 / Security Guide

1. 访问控制
   ```bash
   # 设置访问策略
   curl -X PUT "http://localhost:8001/functions/hello-world/policy" \
        -H "Content-Type: application/json" \
        -d '{
          "version": "2012-10-17",
          "statement": [
            {
              "effect": "Allow",
              "principal": {"AWS": ["arn:aws:iam::123456789012:user/alice"]},
              "action": ["lambda:InvokeFunction"]
            }
          ]
        }'
   ```

2. 加密配置
   ```bash
   # 加密环境变量
   curl -X PUT "http://localhost:8001/functions/hello-world/secrets" \
        -H "Content-Type: application/json" \
        -d '{
          "DB_PASSWORD": "encrypted_value"
        }'
   ```

3. 网络隔离
   ```bash
   # 配置 VPC
   curl -X PUT "http://localhost:8001/functions/hello-world/network" \
        -H "Content-Type: application/json" \
        -d '{
          "vpc": {
            "subnets": ["subnet-12345678"],
            "securityGroups": ["sg-12345678"]
          }
        }'
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