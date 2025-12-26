# Ubuntu 服务器部署指南

本指南将帮助您将 Agent Framework 网站部署到 Ubuntu 服务器上。

## 前置要求

- Ubuntu 18.04 或更高版本
- 具有 sudo 权限的用户
- 域名（可选，但推荐）

## 步骤 1: 服务器准备

### 1.1 更新系统

```bash
sudo apt update
sudo apt upgrade -y
```

### 1.2 安装 Python 和 pip

```bash
sudo apt install python3 python3-pip python3-venv -y
```

### 1.3 安装其他必要工具

```bash
sudo apt install git nginx supervisor -y
```

### 1.4 安装 PostgreSQL（推荐）或使用 SQLite

**选项 A: 安装 PostgreSQL（生产环境推荐）**

```bash
sudo apt install postgresql postgresql-contrib libpq-dev -y
sudo -u postgres psql -c "CREATE DATABASE agent_framework_db;"
sudo -u postgres psql -c "CREATE USER agent_user WITH PASSWORD 'your_secure_password';"
sudo -u postgres psql -c "ALTER ROLE agent_user SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE agent_user SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE agent_user SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE agent_framework_db TO agent_user;"
```

**选项 B: 使用 SQLite（简单但不推荐生产环境）**

SQLite 已经包含在 Python 中，无需额外安装。

## 步骤 2: 上传项目文件

### 2.1 使用 Git（推荐）

```bash
# 在服务器上创建项目目录
sudo mkdir -p /var/www/agent_framework
sudo chown $USER:$USER /var/www/agent_framework
cd /var/www/agent_framework

# 如果项目在 Git 仓库中
git clone <your-repository-url> .

# 或者使用 scp 上传文件
# 在本地机器上运行：
# scp -r * user@your-server:/var/www/agent_framework/
```

### 2.2 创建虚拟环境

```bash
cd /var/www/agent_framework
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## 步骤 3: 配置项目

### 3.1 配置 settings.py

编辑 `agent_framework/settings.py`：

```python
# 修改以下配置
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com', 'your-server-ip']

# 如果使用 PostgreSQL，修改数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'agent_framework_db',
        'USER': 'agent_user',
        'PASSWORD': 'your_secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 静态文件配置
STATIC_URL = '/static/'
STATIC_ROOT = '/var/www/agent_framework/staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/www/agent_framework/media'

# 安全设置
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# 如果使用 HTTPS（推荐）
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
```

### 3.2 生成新的 SECRET_KEY

```bash
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
# 复制生成的密钥，替换 settings.py 中的 SECRET_KEY
```

### 3.3 运行数据库迁移

```bash
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
```

### 3.4 创建超级用户（可选）

```bash
python manage.py createsuperuser
```

## 步骤 4: 安装和配置 Gunicorn

### 4.1 安装 Gunicorn

```bash
source venv/bin/activate
pip install gunicorn
```

将 Gunicorn 添加到 `requirements.txt`：

```bash
echo "gunicorn" >> requirements.txt
```

### 4.2 测试 Gunicorn

```bash
source venv/bin/activate
gunicorn --bind 0.0.0.0:8000 agent_framework.wsgi:application
```

如果成功，您可以访问 `http://your-server-ip:8000` 查看网站。

### 4.3 创建 Gunicorn 服务文件

创建 systemd 服务文件：

```bash
sudo nano /etc/systemd/system/agent_framework.service
```

添加以下内容：

```ini
[Unit]
Description=Agent Framework Gunicorn daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/agent_framework
ExecStart=/var/www/agent_framework/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/var/www/agent_framework/agent_framework.sock \
          agent_framework.wsgi:application

[Install]
WantedBy=multi-user.target
```

**注意：** 如果您的用户名不是 `www-data`，请相应修改 `User` 和 `Group`。

设置权限：

```bash
sudo chown -R www-data:www-data /var/www/agent_framework
sudo chmod -R 755 /var/www/agent_framework
```

启动并启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl start agent_framework
sudo systemctl enable agent_framework
sudo systemctl status agent_framework
```

## 步骤 5: 配置 Nginx

### 5.1 创建 Nginx 配置文件

```bash
sudo nano /etc/nginx/sites-available/agent_framework
```

添加以下配置：

```nginx
server {
    listen 80;
    server_name your-domain.com your-server-ip;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        alias /var/www/agent_framework/staticfiles/;
    }

    location /media/ {
        alias /var/www/agent_framework/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/agent_framework/agent_framework.sock;
    }
}
```

### 5.2 启用站点

```bash
sudo ln -s /etc/nginx/sites-available/agent_framework /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5.3 配置防火墙（如果使用 UFW）

```bash
sudo ufw allow 'Nginx Full'
sudo ufw status
```

## 步骤 6: 配置 SSL（使用 Let's Encrypt，推荐）

### 6.1 安装 Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 6.2 获取 SSL 证书

```bash
sudo certbot --nginx -d your-domain.com
```

按照提示完成配置。Certbot 会自动更新 Nginx 配置以使用 HTTPS。

## 步骤 7: 定期维护

### 7.1 查看日志

```bash
# Gunicorn 日志
sudo journalctl -u agent_framework -f

# Nginx 错误日志
sudo tail -f /var/log/nginx/error.log

# Nginx 访问日志
sudo tail -f /var/log/nginx/access.log
```

### 7.2 重启服务

```bash
# 重启 Gunicorn
sudo systemctl restart agent_framework

# 重启 Nginx
sudo systemctl restart nginx
```

### 7.3 更新代码后的部署

```bash
cd /var/www/agent_framework
source venv/bin/activate
git pull  # 如果使用 Git
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart agent_framework
```

## 故障排查

### 检查服务状态

```bash
sudo systemctl status agent_framework
sudo systemctl status nginx
```

### 检查权限

```bash
sudo chown -R www-data:www-data /var/www/agent_framework
sudo chmod -R 755 /var/www/agent_framework
```

### 检查端口占用

```bash
sudo netstat -tulpn | grep :80
sudo netstat -tulpn | grep :443
```

## 性能优化建议

1. **使用 PostgreSQL** 而不是 SQLite（生产环境）
2. **配置缓存**（如 Redis）
3. **使用 CDN** 提供静态文件
4. **调整 Gunicorn workers** 数量（通常为 CPU 核心数 * 2 + 1）
5. **启用 Gzip 压缩**（在 Nginx 配置中）
6. **配置数据库连接池**

## 安全建议

1. 定期更新系统和 Python 包
2. 使用强密码
3. 配置防火墙规则
4. 使用 HTTPS
5. 定期备份数据库
6. 监控日志文件
7. 限制 SSH 访问

## 备份策略

```bash
# 备份数据库（PostgreSQL）
sudo -u postgres pg_dump agent_framework_db > backup_$(date +%Y%m%d).sql

# 备份项目文件
tar -czf agent_framework_backup_$(date +%Y%m%d).tar.gz /var/www/agent_framework
```

## 快速部署脚本

您也可以创建一个自动化部署脚本。创建 `deploy.sh`：

```bash
#!/bin/bash
cd /var/www/agent_framework
source venv/bin/activate
git pull
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart agent_framework
echo "Deployment completed!"
```

然后设置执行权限：

```bash
chmod +x deploy.sh
```

