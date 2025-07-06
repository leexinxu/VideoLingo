#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Generate Douyin Cookie
# ------------
# Simple script to generate Douyin cookie
# ------------
"""

import os
import asyncio

try:
    from uploader.douyin_uploader import DouyinUploader
    UPLOADER_AVAILABLE = True
except ImportError:
    UPLOADER_AVAILABLE = False
    print("⚠️ Uploader not available. Please install: pip install playwright")

async def generate_cookie():
    """生成抖音Cookie"""
    if not UPLOADER_AVAILABLE:
        print("❌ Uploader not available")
        print("Please install playwright: pip install playwright")
        print("Then install browsers: playwright install chromium")
        return False
    
    account_file = "cookies/douyin_uploader/account.json"
    
    print("🔐 Generating Douyin cookie...")
    print("📱 Please scan QR code to login to Douyin Creator Center")
    print(f"📁 Cookie will be saved to: {account_file}")
    
    # 创建目录
    os.makedirs(os.path.dirname(account_file), exist_ok=True)
    
    uploader = DouyinUploader()
    success = await uploader.generate_cookie(account_file)
    
    if success:
        print("✅ Cookie generated successfully!")
        print("🔍 Testing cookie validity...")
        
        is_valid = await uploader.check_cookie_auth(account_file)
        if is_valid:
            print("✅ Cookie is valid and ready to use!")
        else:
            print("❌ Cookie is invalid, please try again")
            return False
        
        return True
    else:
        print("❌ Failed to generate cookie")
        return False

async def main():
    """主函数"""
    print("🎬 Douyin Cookie Generator")
    print("=" * 50)
    
    success = await generate_cookie()
    
    if success:
        print("\n✅ Cookie setup completed!")
        print("\n📋 Next steps:")
        print("1. Run playlist_monitor.py to start monitoring")
        print("2. Videos will be automatically uploaded to Douyin")
    else:
        print("\n❌ Cookie setup failed")
        print("Please check the error messages above")

if __name__ == "__main__":
    asyncio.run(main()) 