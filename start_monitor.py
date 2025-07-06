#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Playlist Monitor Starter
# ------------
# Simple script to start the YouTube playlist monitor
# ------------
"""

import os
import sys
import argparse
from playlist_monitor import PlaylistMonitor

def main():
    parser = argparse.ArgumentParser(description='YouTube Playlist Monitor')
    parser.add_argument('--interval', '-i', type=int, default=60, 
                       help='Check interval in seconds (default: 60)')
    parser.add_argument('--test', '-t', action='store_true',
                       help='Test mode - check playlists once and exit')
    parser.add_argument('--proxy', '-p', action='store_true',
                       help='Enable proxy for YouTube downloads')
    
    args = parser.parse_args()
    
    print("🎬 YouTube Playlist Monitor Starter")
    print("=" * 50)
    
    # 检查配置文件
    if not os.path.exists("config.yaml"):
        print("❌ config.yaml not found. Please run the setup first.")
        print("You can run: streamlit run st.py to configure settings.")
        return
    
    # 创建监控器实例
    monitor = PlaylistMonitor()
    
    # 如果启用代理，更新代理配置
    if args.proxy:
        print("🌐 Proxy enabled for YouTube downloads")
        if monitor.proxy_config.get("proxy_settings", {}).get("enabled", False):
            print(f"Using proxy: {monitor.proxy_config['proxy_settings']['https_proxy']}")
        else:
            print("⚠️ Proxy config not found or disabled. Please check proxy_config.json")
    
    if args.test:
        print("🧪 Test mode - checking playlists once...")
        import asyncio
        asyncio.run(monitor.check_playlists())
        print("✅ Test completed!")
    else:
        print(f"🚀 Starting monitor with {args.interval} second interval...")
        import asyncio
        asyncio.run(monitor.run_monitor(args.interval))

if __name__ == "__main__":
    main() 