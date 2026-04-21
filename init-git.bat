@echo off
echo ========================================
echo ONCITY-Django Git 初始化脚本
echo ========================================
echo.

REM 检查是否已存在 .git 目录
if exist .git (
    echo [警告] Git 仓库已存在！
    echo 如果要重新初始化，请先删除 .git 文件夹
    pause
    exit /b
)

echo [1/5] 初始化 Git 仓库...
git init
if errorlevel 1 (
    echo [错误] Git 初始化失败！请确保已安装 Git
    pause
    exit /b
)

echo [2/5] 添加所有文件到暂存区...
git add .

echo [3/5] 创建初始提交...
git commit -m "Initial commit: Django backend project"

echo.
echo [4/5] 请在 GitHub 上创建新仓库，然后输入仓库地址
echo 示例: https://github.com/yourusername/oncity-backend.git
echo.
set /p REMOTE_URL="输入 GitHub 仓库地址: "

if "%REMOTE_URL%"=="" (
    echo [提示] 未输入地址，跳过远程仓库配置
    echo 你可以稍后手动执行: git remote add origin YOUR_REPO_URL
) else (
    echo [5/5] 关联远程仓库并推送...
    git remote add origin %REMOTE_URL%
    git branch -M main
    git push -u origin main
    
    if errorlevel 1 (
        echo [错误] 推送失败！请检查网络连接和仓库地址
        pause
        exit /b
    )
)

echo.
echo ========================================
echo ✓ 完成！代码已成功推送到 GitHub
echo ========================================
pause
