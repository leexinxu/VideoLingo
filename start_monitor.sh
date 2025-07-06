#!/bin/bash

echo "🎬 YouTube Playlist Monitor Starter"
echo "========================================"

# 检查conda环境
if command -v conda &> /dev/null; then
    source $(conda info --base)/etc/profile.d/conda.sh
    conda activate videolingo
else
    echo "❌ conda not found. Please install conda first."
    exit 1
fi

# 检查配置文件
if [ ! -f "config.yaml" ]; then
    echo "❌ config.yaml not found. Please run the setup first."
    echo "You can run: streamlit run st.py to configure settings."
    exit 1
fi

# 启动监控器
echo "🚀 Starting YouTube Playlist Monitor..."
echo "Press Ctrl+C to stop"
echo

# 检查是否启用代理
if [[ "$1" == "--proxy" ]]; then
    echo "🌐 Proxy mode enabled"
    python start_monitor.py --proxy "$@"
else
    python start_monitor.py "$@"
fi 