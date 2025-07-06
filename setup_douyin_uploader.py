#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Douyin Uploader Setup
# ------------
# Setup script for Douyin uploader
# ------------
"""

import os
import json
import asyncio
from pathlib import Path

try:
    from uploader.douyin_uploader import DouyinUploader
    UPLOADER_AVAILABLE = True
except ImportError:
    UPLOADER_AVAILABLE = False
    print("⚠️ Uploader not available. Please install: pip install playwright")

async def setup_douyin_uploader():
    """设置抖音上传器"""
    print("🎬 Douyin Uploader Setup")
    print("=" * 50)
    
    if not UPLOADER_AVAILABLE:
        print("❌ Uploader not available")
        print("Please install playwright: pip install playwright")
        print("Then install browsers: playwright install chromium")
        return False
    
    # 加载当前配置
    config_file = "uploader_config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {
            "douyin": {
                "enabled": False,
                "account_file": "cookies/douyin_uploader/account.json",
                "auto_upload": False,
                "schedule_time": "16:00",
                "location": "杭州市",
                "tags": ["VideoLingo", "AI翻译", "视频配音"],
                "chrome_path": None
            },
            "upload_settings": {
                "max_title_length": 30,
                "max_tags": 10,
                "retry_times": 3,
                "wait_time": 2
            }
        }
    
    print("\n📋 Current Configuration:")
    print(f"  Enabled: {config['douyin']['enabled']}")
    print(f"  Auto Upload: {config['douyin']['auto_upload']}")
    print(f"  Schedule Time: {config['douyin']['schedule_time']}")
    print(f"  Location: {config['douyin']['location']}")
    print(f"  Tags: {config['douyin']['tags']}")
    
    # 询问是否启用抖音上传
    enable = input("\n❓ Enable Douyin upload? (y/n): ").lower().strip()
    if enable == 'y':
        config['douyin']['enabled'] = True
        
        # 询问是否自动上传
        auto_upload = input("❓ Enable auto upload? (y/n): ").lower().strip()
        if auto_upload == 'y':
            config['douyin']['auto_upload'] = True
            
            # 设置发布时间
            schedule_time = input("❓ Schedule time (HH:MM, default 16:00): ").strip()
            if schedule_time:
                config['douyin']['schedule_time'] = schedule_time
        
        # 设置位置
        location = input("❓ Location (default 杭州市): ").strip()
        if location:
            config['douyin']['location'] = location
        
        # 设置标签
        print("\n📝 Current tags:", config['douyin']['tags'])
        add_tags = input("❓ Add more tags? (comma separated): ").strip()
        if add_tags:
            new_tags = [tag.strip() for tag in add_tags.split(',')]
            config['douyin']['tags'].extend(new_tags)
        
        # 设置Chrome路径（可选）
        chrome_path = input("❓ Chrome executable path (optional): ").strip()
        if chrome_path:
            config['douyin']['chrome_path'] = chrome_path
        
        # 保存配置
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        
        print("\n✅ Configuration saved!")
        
        # 设置Cookie
        print("\n🔐 Setting up Douyin authentication...")
        return await setup_douyin_cookie(config['douyin']['account_file'])
    
    return True

async def setup_douyin_cookie(account_file: str):
    """设置抖音Cookie"""
    print(f"📁 Cookie file: {account_file}")
    
    # 创建目录
    os.makedirs(os.path.dirname(account_file), exist_ok=True)
    
    # 检查现有Cookie
    if os.path.exists(account_file):
        print("📋 Existing cookie file found")
        check = input("❓ Check if cookie is valid? (y/n): ").lower().strip()
        if check == 'y':
            uploader = DouyinUploader()
            is_valid = await uploader.check_cookie_auth(account_file)
            if is_valid:
                print("✅ Cookie is valid!")
                return True
            else:
                print("❌ Cookie is invalid")
                regenerate = input("❓ Regenerate cookie? (y/n): ").lower().strip()
                if regenerate != 'y':
                    return False
    
    # 生成新Cookie
    print("\n🔐 Generating new Douyin cookie...")
    print("📱 Please scan QR code to login to Douyin Creator Center")
    
    uploader = DouyinUploader()
    success = await uploader.generate_cookie(account_file)
    
    if success:
        print("✅ Cookie generated successfully!")
        return True
    else:
        print("❌ Failed to generate cookie")
        return False

async def main():
    """主函数"""
    print("🎬 Douyin Uploader Setup for VideoLingo")
    print("=" * 50)
    
    success = await setup_douyin_uploader()
    
    if success:
        print("\n✅ Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Edit uploader_config.json to customize settings")
        print("2. Run playlist_monitor.py to start monitoring")
        print("3. Videos will be automatically uploaded to Douyin")
    else:
        print("\n❌ Setup failed")
        print("Please check the error messages above")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 