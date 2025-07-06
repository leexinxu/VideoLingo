@echo off
chcp 65001 >nul
echo 🎬 YouTube Playlist Monitor Starter
echo ========================================

REM 检查conda环境
call conda activate videolingo

REM 检查配置文件
if not exist "config.yaml" (
    echo ❌ config.yaml not found. Please run the setup first.
    echo You can run: streamlit run st.py to configure settings.
    pause
    exit /b 1
)

REM 启动监控器
echo 🚀 Starting YouTube Playlist Monitor...
echo Press Ctrl+C to stop
echo.

REM 检查是否启用代理
if "%1"=="--proxy" (
    echo 🌐 Proxy mode enabled
    python start_monitor.py --proxy %*
) else (
    python start_monitor.py %*
)

pause 