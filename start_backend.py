#!/usr/bin/env python3
"""
ONCITY Backend One-Click Starter
自动处理: venv创建、依赖安装、.env配置、logs目录、MySQL连接检测、数据库迁移、服务器启动
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
VENV_DIR = BASE_DIR / "venv"
REQUIREMENTS = BASE_DIR / "requirements.txt"
ENV_FILE = BASE_DIR / ".env"
ENV_EXAMPLE = BASE_DIR / ".env.example"
LOGS_DIR = BASE_DIR / "logs"
MANAGE_PY = BASE_DIR / "manage.py"


def get_venv_python():
    """获取虚拟环境中的 Python 路径"""
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def get_venv_pip():
    """获取虚拟环境中的 pip 路径"""
    if sys.platform == "win32":
        return VENV_DIR / "Scripts" / "pip.exe"
    return VENV_DIR / "bin" / "pip"


def run(cmd, cwd=None, check=True):
    """运行命令并返回结果"""
    print(f"  $ {' '.join(str(c) for c in cmd)}")
    result = subprocess.run(cmd, cwd=cwd or BASE_DIR, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr and "RuntimeWarning" not in result.stderr:
        # 过滤掉常见的无害警告
        stderr_clean = result.stderr
        if "Using password" in stderr_clean or "access denied" in stderr_clean.lower():
            pass  # MySQL 错误会在后面单独处理
        elif "Watching for file changes" in stderr_clean:
            print(stderr_clean.strip())
    if check and result.returncode != 0:
        return result
    return result


def step_header(title):
    """打印步骤标题"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}")


def create_venv():
    """创建虚拟环境"""
    if VENV_DIR.exists():
        print("  虚拟环境已存在，跳过创建")
        return True
    print("  正在创建虚拟环境...")
    result = subprocess.run([sys.executable, "-m", "venv", str(VENV_DIR)], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  创建虚拟环境失败: {result.stderr}")
        return False
    print("  虚拟环境创建成功")
    return True


def install_deps():
    """安装依赖"""
    pip = get_venv_pip()
    print("  正在安装依赖（可能需要几分钟）...")
    result = subprocess.run([str(pip), "install", "-r", str(REQUIREMENTS)], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  安装依赖失败: {result.stderr}")
        return False
    print("  依赖安装完成")
    return True


def setup_env():
    """配置 .env 文件"""
    if ENV_FILE.exists():
        print("  .env 文件已存在")
        # 检查密码是否还是默认值
        content = ENV_FILE.read_text(encoding="utf-8")
        if "DB_PASSWORD=your_mysql_password" in content:
            print("  检测到 MySQL 密码为默认值，需要配置")
            return False
        return True

    if not ENV_EXAMPLE.exists():
        print("  错误: .env.example 文件不存在")
        return False

    print("  从 .env.example 创建 .env 文件...")
    shutil.copy(ENV_EXAMPLE, ENV_FILE)
    print("  .env 文件已创建，请配置 MySQL 密码后重新运行")
    return False


def fix_mysql_password():
    """修复 MySQL 密码"""
    print("\n  请输入本地 MySQL root 用户的密码:")
    password = input("  MySQL Password: ").strip()
    if not password:
        print("  密码不能为空")
        return False

    content = ENV_FILE.read_text(encoding="utf-8")
    content = content.replace("DB_PASSWORD=your_mysql_password", f"DB_PASSWORD={password}")
    ENV_FILE.write_text(content, encoding="utf-8")
    print("  密码已写入 .env 文件")
    return True


def create_logs_dir():
    """创建 logs 目录"""
    if LOGS_DIR.exists():
        print("  logs 目录已存在")
        return True
    LOGS_DIR.mkdir(exist_ok=True)
    print("  logs 目录已创建")
    return True


def test_mysql_connection():
    """测试 MySQL 连接"""
    print("  正在测试 MySQL 连接...")
    venv_python = get_venv_python()

    # 读取 .env 中的数据库配置
    db_config = {}
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            if line.startswith("DB_") and "=" in line:
                key, val = line.split("=", 1)
                db_config[key] = val.strip()

    host = db_config.get("DB_HOST", "localhost")
    port = int(db_config.get("DB_PORT", "3306"))
    user = db_config.get("DB_USER", "root")
    password = db_config.get("DB_PASSWORD", "")
    db_name = db_config.get("DB_NAME", "oncity_db")

    test_script = f"""
import sys
try:
    import MySQLdb
    conn = MySQLdb.connect(host='{host}', port={port}, user='{user}', password='{password}', db='{db_name}')
    conn.close()
    print('OK')
except Exception as e:
    print('FAIL:', e)
    sys.exit(1)
"""
    result = subprocess.run([str(venv_python), "-c", test_script], capture_output=True, text=True)
    stdout = result.stdout.strip()

    if stdout == "OK":
        print("  MySQL 连接成功")
        return True
    else:
        print(f"  MySQL 连接失败: {stdout}")
        return False


def run_migrations():
    """运行数据库迁移"""
    venv_python = get_venv_python()
    print("  正在创建迁移文件...")
    subprocess.run([str(venv_python), str(MANAGE_PY), "makemigrations"], cwd=BASE_DIR, capture_output=True)
    print("  正在执行数据库迁移...")
    result = subprocess.run([str(venv_python), str(MANAGE_PY), "migrate"], cwd=BASE_DIR, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  迁移失败: {result.stderr}")
        return False
    print("  数据库迁移完成")
    return True


def start_server():
    """启动开发服务器"""
    venv_python = get_venv_python()
    print("\n" + "="*50)
    print("  Django 开发服务器已启动")
    print("  URL:     http://127.0.0.1:8000")
    print("  Admin:   http://127.0.0.1:8000/admin/")
    print("  Health:  http://127.0.0.1:8000/api/health")
    print("="*50)
    print("  按 Ctrl+C 停止服务器\n")

    # 使用 os.system 或 subprocess.run 前台运行，让用户可以看到输出并按 Ctrl+C 停止
    try:
        subprocess.run([str(venv_python), str(MANAGE_PY), "runserver", "0.0.0.0:8000"], cwd=BASE_DIR)
    except KeyboardInterrupt:
        print("\n  服务器已停止")


def main():
    print(r"""
   ____  _   _ ____   _____  _   _ _______   __
  / __ \| \ | / __ \ / ___ || | | |_   _\ \ / /
 | |  | |  V / |  | | |   | | | | | | |  \ V /
 | |__| | |\ \ |__| | |___| | |_| | | |   | |
  \____/|_| \_\____/ \_____| \___/  |_|   |_|
""")
    print("  ONCITY 后端一键启动脚本")

    # Step 1: 虚拟环境
    step_header("Step 1/6: 检查虚拟环境")
    if not create_venv():
        sys.exit(1)

    # Step 2: 依赖安装
    step_header("Step 2/6: 安装依赖")
    if not install_deps():
        sys.exit(1)

    # Step 3: .env 配置
    step_header("Step 3/6: 检查 .env 配置")
    if not setup_env():
        if ENV_FILE.exists() and "DB_PASSWORD=your_mysql_password" in ENV_FILE.read_text(encoding="utf-8"):
            if not fix_mysql_password():
                sys.exit(1)
        else:
            sys.exit(1)

    # Step 4: logs 目录
    step_header("Step 4/6: 检查 logs 目录")
    create_logs_dir()

    # Step 5: MySQL 连接 & 迁移
    step_header("Step 5/6: 测试数据库连接并执行迁移")
    if not test_mysql_connection():
        print("\n  请检查:")
        print("  1. MySQL 服务是否已启动")
        print("  2. .env 中的 DB_PASSWORD 是否正确")
        print("  3. 数据库 'oncity_db' 是否存在（如果不存在，Django 不会自动创建数据库）")
        print("\n  如果需要创建数据库，请在 MySQL 中执行:")
        print("  CREATE DATABASE oncity_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        sys.exit(1)

    if not run_migrations():
        sys.exit(1)

    # Step 6: 启动服务器
    step_header("Step 6/6: 启动开发服务器")
    start_server()


if __name__ == "__main__":
    main()
