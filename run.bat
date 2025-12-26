@echo off
echo 启动 Agent Framework 开发服务器...
call venv\Scripts\activate.bat
python manage.py runserver
pause

