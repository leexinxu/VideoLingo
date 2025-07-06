#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Douyin Uploader Test
# ------------
# Test script for Douyin uploader
# ------------
"""

import os
import json
import asyncio
from pathlib import Path

def test_config():
    """测试配置文件"""
    print("🔧 Testing configuration...")
    
    # 检查配置文件
    config_file = "uploader_config.json"
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print("✅ Configuration file found")
            print(f"   Douyin enabled: {config.get('douyin', {}).get('enabled', False)}")
            print(f"   Auto upload: {config.get('douyin', {}).get('auto_upload', False)}")
            return True
        except Exception as e:
            print(f"❌ Error reading config: {e}")
            return False
    else:
        print("❌ Configuration file not found")
        return False

def test_dependencies():
    """测试依赖"""
    print("\n📦 Testing dependencies...")
    
    # 检查Playwright
    try:
        import playwright
        print("✅ Playwright installed")
    except ImportError:
        print("❌ Playwright not installed")
        print("   Run: pip install playwright")
        return False
    
    # 检查上传器模块
    try:
        from uploader.douyin_uploader import DouyinUploader
        print("✅ Uploader module available")
        return True
    except ImportError as e:
        print(f"❌ Uploader module error: {e}")
        return False

async def test_cookie():
    """测试Cookie"""
    print("\n🍪 Testing Douyin cookie...")
    
    try:
        from uploader.douyin_uploader import DouyinUploader
        
        config_file = "uploader_config.json"
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            account_file = config.get('douyin', {}).get('account_file', 'cookies/douyin_uploader/account.json')
            
            if os.path.exists(account_file):
                uploader = DouyinUploader()
                is_valid = await uploader.check_cookie_auth(account_file)
                if is_valid:
                    print("✅ Cookie is valid")
                    return True
                else:
                    print("❌ Cookie is invalid")
                    return False
            else:
                print("❌ Cookie file not found")
                return False
        else:
            print("❌ Configuration file not found")
            return False
            
    except Exception as e:
        print(f"❌ Cookie test error: {e}")
        return False

def test_video_files():
    """测试视频文件"""
    print("\n🎬 Testing video files...")
    
    # 检查历史文件夹中的视频文件
    history_dir = "history"
    if not os.path.exists(history_dir):
        print("❌ History directory not found")
        return False
    
    found_videos = []
    for playlist_dir in os.listdir(history_dir):
        playlist_path = os.path.join(history_dir, playlist_dir)
        if os.path.isdir(playlist_path):
            for video_dir in os.listdir(playlist_path):
                video_path = os.path.join(playlist_path, video_dir)
                if os.path.isdir(video_path):
                    # 查找输出视频文件
                    if playlist_dir == "中字":
                        video_file = os.path.join(video_path, "output_sub.mp4")
                    elif playlist_dir == "中配":
                        video_file = os.path.join(video_path, "output_dub.mp4")
                    else:
                        continue
                    
                    if os.path.exists(video_file):
                        found_videos.append({
                            'file': video_file,
                            'playlist': playlist_dir,
                            'size': os.path.getsize(video_file)
                        })
    
    if found_videos:
        print(f"✅ Found {len(found_videos)} video files:")
        for video in found_videos:
            size_mb = video['size'] / (1024 * 1024)
            print(f"   {video['playlist']}: {os.path.basename(video['file'])} ({size_mb:.1f}MB)")
        return True
    else:
        print("❌ No video files found")
        return False

async def test_uploader():
    """测试上传器"""
    print("\n🚀 Testing uploader...")
    
    try:
        from uploader.douyin_uploader import DouyinUploader
        
        uploader = DouyinUploader()
        print("✅ Uploader initialized")
        
        # 检查配置
        config = uploader.config
        print(f"   Douyin enabled: {config['douyin']['enabled']}")
        print(f"   Auto upload: {config['douyin']['auto_upload']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Uploader test error: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 Douyin Uploader Test")
    print("=" * 50)
    
    # 运行测试
    tests = [
        ("Configuration", test_config),
        ("Dependencies", test_dependencies),
        ("Cookie", lambda: asyncio.run(test_cookie())),
        ("Video Files", test_video_files),
        ("Uploader", lambda: asyncio.run(test_uploader()))
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed: {e}")
            results.append((test_name, False))
    
    # 显示结果
    print("\n📊 Test Results:")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:15} {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {len(results)} tests, {passed} passed, {len(results) - passed} failed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! Uploader is ready to use.")
    else:
        print("\n⚠️ Some tests failed. Please check the issues above.")
        print("\n💡 Setup instructions:")
        print("1. Run: python setup_douyin_uploader.py")
        print("2. Install playwright: pip install playwright")
        print("3. Install browsers: playwright install chromium")

if __name__ == "__main__":
    main() 