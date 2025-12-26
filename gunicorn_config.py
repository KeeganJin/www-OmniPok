# Gunicorn 配置文件
# 使用方式: gunicorn -c gunicorn_config.py agent_framework.wsgi:application

import multiprocessing

# 服务器socket
bind = "unix:/var/www/agent_framework/agent_framework.sock"

# 工作进程数
workers = multiprocessing.cpu_count() * 2 + 1

# 工作模式
worker_class = "sync"

# 工作进程超时时间（秒）
timeout = 120

# 保持活跃的连接数
keepalive = 2

# 日志级别
loglevel = "info"

# 访问日志文件路径（'-' 表示标准输出）
accesslog = "-"

# 错误日志文件路径（'-' 表示标准错误）
errorlog = "-"

# 进程名
proc_name = "agent_framework"

# 守护进程模式（在 systemd 中运行时设为 False）
daemon = False

# 用户和组（在 systemd 中由 service 文件设置，这里注释掉）
# user = "www-data"
# group = "www-data"

# 临时文件目录
tmp_upload_dir = None

# 预加载应用（可以提高性能，但会增加内存使用）
preload_app = False

# 最大请求数（达到后重启 worker）
max_requests = 1000
max_requests_jitter = 50

