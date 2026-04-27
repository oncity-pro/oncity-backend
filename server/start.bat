@echo off
REM ONCITY-Django Backend One-Click Starter for Windows
REM 自动处理: venv、依赖、.env、logs、MySQL检测、迁移、启动

echo ========================================
echo   ONCITY 后端一键启动
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python，请先安装 Python 3.13+
    pause
    exit /b 1
)

REM 运行一键启动脚本
python start_backend.py
