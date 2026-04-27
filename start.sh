#!/bin/bash
# ONCITY-Django Backend One-Click Starter for Linux/Mac
# 自动处理: venv、依赖、.env、logs、MySQL检测、迁移、启动

echo "========================================"
echo "  ONCITY 后端一键启动"
echo "========================================"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 python3，请先安装 Python 3.13+"
    exit 1
fi

# 运行一键启动脚本
python3 start_backend.py
