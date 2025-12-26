#!/bin/bash
# Agent Framework 快速部署脚本
# 使用方法: ./deploy.sh

echo "=== Agent Framework 部署脚本 ==="

# 检查是否在正确的目录
if [ ! -f "manage.py" ]; then
    echo "错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 激活虚拟环境
if [ -d "venv" ]; then
    echo "激活虚拟环境..."
    source venv/bin/activate
else
    echo "错误: 虚拟环境不存在，请先创建: python3 -m venv venv"
    exit 1
fi

# 更新代码（如果使用 Git）
if [ -d ".git" ]; then
    echo "更新代码..."
    git pull
fi

# 安装/更新依赖
echo "安装依赖..."
pip install -r requirements.txt

# 运行数据库迁移
echo "运行数据库迁移..."
python manage.py migrate

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 重启 Gunicorn 服务（如果存在）
if systemctl is-active --quiet agent_framework; then
    echo "重启 Gunicorn 服务..."
    sudo systemctl restart agent_framework
else
    echo "提示: Gunicorn 服务未运行或不存在"
fi

echo "=== 部署完成! ==="

