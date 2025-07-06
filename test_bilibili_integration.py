#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Test Bilibili Integration
# ------------
# 测试bilibili上传集成
# ------------
"""

import os
import sys
import asyncio
import json
from pathlib import Path

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def test_bilibili_uploader_import():
    """测试bilibili上传器导入"""
    print("🧪 Testing Bilibili uploader import...")
    
    try:
        from uploader.bilibili_uploader import BilibiliUploader
        print("✅ Bilibili uploader imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Failed to import Bilibili uploader: {e}")
        return False

def test_bilibili_config():
    """测试bilibili配置"""
    print("\n🧪 Testing Bilibili configuration...")
    
    # 检查配置文件
    config_file = Path("uploader_config.json")
    if not config_file.exists():
        print("❌ uploader_config.json not found")
        return False
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        bilibili_config = config.get("bilibili", {})
        print(f"📋 Bilibili config: {bilibili_config}")
        
        if bilibili_config.get("enabled", False):
            print("✅ Bilibili uploader is enabled")
        else:
            print("⚠️ Bilibili uploader is disabled")
        
        return True
    except Exception as e:
        print(f"❌ Error reading config: {e}")
        return False

def test_bilibili_cookie():
    """测试bilibili cookie文件"""
    print("\n🧪 Testing Bilibili cookie file...")
    
    cookie_file = Path("uploader_config/bilibili_cookies.json")
    if not cookie_file.exists():
        print(f"❌ Cookie file not found: {cookie_file}")
        print("Please run: python setup_bilibili.py")
        return False
    
    try:
        with open(cookie_file, 'r', encoding='utf-8') as f:
            cookie_data = json.load(f)
        
        # 检查必要的字段
        required_fields = ["SESSDATA", "bili_jct", "DedeUserID"]
        cookie_info = cookie_data.get("cookie_info", {})
        cookies = cookie_info.get("cookies", [])
        
        cookie_dict = {}
        for cookie in cookies:
            cookie_dict[cookie.get("name")] = cookie.get("value")
        
        missing_fields = [field for field in required_fields if field not in cookie_dict]
        if missing_fields:
            print(f"❌ Missing required cookie fields: {missing_fields}")
            return False
        
        print("✅ Cookie file is valid")
        return True
    except Exception as e:
        print(f"❌ Error reading cookie file: {e}")
        return False

async def test_playlist_monitor_integration():
    """测试播放列表监控器集成"""
    print("\n🧪 Testing playlist monitor integration...")
    
    try:
        from playlist_monitor import PlaylistMonitor
        
        monitor = PlaylistMonitor()
        
        # 检查bilibili上传器可用性
        if hasattr(monitor, 'uploader_config'):
            bilibili_config = monitor.uploader_config.get("bilibili", {})
            print(f"📋 Bilibili config in monitor: {bilibili_config}")
            
            if bilibili_config.get("enabled", False):
                print("✅ Bilibili uploader is enabled in monitor")
            else:
                print("⚠️ Bilibili uploader is disabled in monitor")
        
        print("✅ Playlist monitor integration test passed")
        return True
    except Exception as e:
        print(f"❌ Playlist monitor integration test failed: {e}")
        return False

def test_biliup_installation():
    """测试biliup安装"""
    print("\n🧪 Testing biliup installation...")
    
    try:
        import biliup
        print("✅ biliup is installed")
        return True
    except ImportError:
        print("❌ biliup is not installed")
        print("Please run: pip install biliup")
        return False

async def main():
    """主测试函数"""
    print("🧪 Starting Bilibili Integration Tests...")
    print("=" * 60)
    
    tests = [
        ("Biliup Installation", test_biliup_installation),
        ("Bilibili Uploader Import", test_bilibili_uploader_import),
        ("Bilibili Configuration", test_bilibili_config),
        ("Bilibili Cookie File", test_bilibili_cookie),
        ("Playlist Monitor Integration", test_playlist_monitor_integration),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # 显示测试结果
    print(f"\n{'='*60}")
    print("📊 Test Results:")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<30} {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Bilibili integration is ready.")
        print("\n💡 You can now upload videos to both Douyin and Bilibili!")
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        print("\n🔧 To fix issues:")
        print("1. Install biliup: pip install biliup")
        print("2. Run setup: python setup_bilibili.py")
        print("3. Configure cookies in uploader_config/bilibili_cookies.json")

if __name__ == "__main__":
    asyncio.run(main()) 