# 部署检查清单

## 服务器准备
- [ ] 更新系统包 (`sudo apt update && sudo apt upgrade -y`)
- [ ] 安装 Python3、pip、venv
- [ ] 安装 Nginx
- [ ] 安装 PostgreSQL（可选，推荐）或使用 SQLite
- [ ] 配置防火墙（UFW）

## 项目部署
- [ ] 上传项目文件到服务器（建议：`/var/www/agent_framework`）
- [ ] 创建虚拟环境 (`python3 -m venv venv`)
- [ ] 激活虚拟环境并安装依赖 (`pip install -r requirements.txt`)
- [ ] 配置 `settings.py`:
  - [ ] 设置 `DEBUG = False`
  - [ ] 设置 `ALLOWED_HOSTS`
  - [ ] 生成新的 `SECRET_KEY`
  - [ ] 配置数据库（如果使用 PostgreSQL）
  - [ ] 配置 `STATIC_ROOT` 和 `MEDIA_ROOT`
- [ ] 运行数据库迁移 (`python manage.py migrate`)
- [ ] 收集静态文件 (`python manage.py collectstatic --noinput`)
- [ ] 创建超级用户（可选）

## Gunicorn 配置
- [ ] 安装 Gunicorn (`pip install gunicorn`)
- [ ] 测试 Gunicorn 是否正常工作
- [ ] 创建 systemd 服务文件 (`/etc/systemd/system/agent_framework.service`)
- [ ] 设置正确的文件权限 (`sudo chown -R www-data:www-data /var/www/agent_framework`)
- [ ] 启动并启用服务 (`sudo systemctl start agent_framework && sudo systemctl enable agent_framework`)

## Nginx 配置
- [ ] 创建 Nginx 配置文件 (`/etc/nginx/sites-available/agent_framework`)
- [ ] 创建符号链接到 `sites-enabled`
- [ ] 测试 Nginx 配置 (`sudo nginx -t`)
- [ ] 重启 Nginx (`sudo systemctl restart nginx`)

## SSL 配置（推荐）
- [ ] 安装 Certbot (`sudo apt install certbot python3-certbot-nginx`)
- [ ] 获取 SSL 证书 (`sudo certbot --nginx -d your-domain.com`)
- [ ] 验证证书自动续期是否配置

## 安全设置
- [ ] 检查文件权限
- [ ] 配置防火墙规则
- [ ] 设置强密码
- [ ] 定期备份数据库
- [ ] 配置日志监控

## 测试
- [ ] 访问网站首页
- [ ] 测试所有页面路由
- [ ] 检查静态文件是否正常加载
- [ ] 检查日志文件是否有错误
- [ ] 测试 HTTPS（如果配置了 SSL）

## 后续维护
- [ ] 设置自动备份脚本
- [ ] 配置日志轮转
- [ ] 设置监控和告警
- [ ] 定期更新系统和依赖包

