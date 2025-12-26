# Agent Framework 介绍网站

这是一个用 Django 开发的 Agent Framework 介绍网站。

## 功能特性

- 🏠 首页：展示框架的概览和核心特性
- 📋 特性页面：详细介绍框架的各项功能
- 📚 文档页面：提供使用文档和API参考

## 快速开始

### 1. 创建并激活虚拟环境

**Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 运行数据库迁移

```bash
python manage.py migrate
```

### 4. 创建超级用户（可选）

```bash
python manage.py createsuperuser
```

### 5. 启动开发服务器

```bash
python manage.py runserver
```

### 6. 访问网站

在浏览器中打开 `http://127.0.0.1:8000/`

## 项目结构

```
.
├── agent_framework/          # Django 项目配置
│   ├── __init__.py
│   ├── settings.py           # 项目设置
│   ├── urls.py               # URL 路由配置
│   ├── wsgi.py
│   └── asgi.py
├── framework/                # 主要应用
│   ├── __init__.py
│   ├── apps.py
│   ├── views.py              # 视图函数
│   ├── urls.py
│   └── templates/            # HTML 模板
│       └── framework/
│           ├── base.html
│           ├── index.html
│           ├── features.html
│           └── documentation.html
├── static/                   # 静态文件
│   └── css/
│       └── style.css
├── manage.py                 # Django 管理脚本
├── requirements.txt          # Python 依赖
└── README.md                 # 项目说明
```

## 页面说明

- `/` - 首页，展示框架介绍和快速开始
- `/features/` - 特性页面，详细介绍框架功能
- `/documentation/` - 文档页面，提供使用文档
- `/admin/` - Django 管理后台

## 技术栈

- Django 4.2+
- HTML5
- CSS3 (现代响应式设计)
- Python 3.8+

## 开发说明

这是一个演示项目，展示了如何使用 Django 快速开发一个介绍网站。网站采用了现代化的设计，包括：

- 响应式布局，支持移动端
- 美观的UI设计
- 清晰的导航结构
- 代码示例展示

## 部署到生产环境

详细的 Ubuntu 服务器部署指南请参考 [DEPLOYMENT.md](DEPLOYMENT.md)

快速部署步骤：

1. 将项目上传到服务器
2. 创建虚拟环境并安装依赖
3. 配置 `settings.py`（设置 `DEBUG=False` 和 `ALLOWED_HOSTS`）
4. 运行 `python manage.py migrate` 和 `python manage.py collectstatic`
5. 配置 Gunicorn 和 Nginx
6. 启动服务

## 许可证

MIT License

