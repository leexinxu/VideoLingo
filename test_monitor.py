#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ------------
# Monitor Test Script
# ------------
# Test script to verify playlist monitor functionality
# ------------
"""

import os
import sys
import json
from playlist_monitor import PlaylistMonitor

def test_config():
    """测试配置文件"""
    print("🔧 Testing configuration...")
    
    # 检查config.yaml
    if not os.path.exists("config.yaml"):
        print("❌ config.yaml not found")
        return False
    print("✅ config.yaml found")
    
    # 检查playlist_monitor_config.json
    if not os.path.exists("playlist_monitor_config.json"):
        print("❌ playlist_monitor_config.json not found")
        return False
    print("✅ playlist_monitor_config.json found")
    
    return True

def test_imports():
    """测试导入"""
    print("📦 Testing imports...")
    
    try:
        import core.st_utils.imports_and_utils
        print("✅ Core imports successful")
    except Exception as e:
        print(f"❌ Core imports failed: {e}")
        return False
    
    try:
        import core
        print("✅ Core modules imported")
    except Exception as e:
        print(f"❌ Core modules import failed: {e}")
        return False
    
    return True

def test_playlist_access():
    """测试播放列表访问"""
    print("🌐 Testing playlist access...")
    
    monitor = PlaylistMonitor()
    
    for playlist_name, playlist_config in monitor.playlists.items():
        print(f"Testing playlist: {playlist_name}")
        try:
            videos = monitor.get_playlist_videos(playlist_config['url'])
            if videos:
                print(f"✅ {playlist_name}: Found {len(videos)} videos")
            else:
                print(f"⚠️ {playlist_name}: No videos found")
        except Exception as e:
            print(f"❌ {playlist_name}: Error accessing playlist - {e}")
            return False
    
    return True

def test_output_directories():
    """测试输出目录"""
    print("📁 Testing output directories...")
    
    directories = ["output", "playlist_monitor", "history"]
    
    for directory in directories:
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
                print(f"✅ Created directory: {directory}")
            except Exception as e:
                print(f"❌ Failed to create directory {directory}: {e}")
                return False
        else:
            print(f"✅ Directory exists: {directory}")
    
    return True

def main():
    """主测试函数"""
    print("🧪 YouTube Playlist Monitor Test")
    print("=" * 50)
    
    tests = [
        ("Configuration", test_config),
        ("Imports", test_imports),
        ("Output Directories", test_output_directories),
        ("Playlist Access", test_playlist_access),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} Test ---")
        if test_func():
            print(f"✅ {test_name} test passed")
            passed += 1
        else:
            print(f"❌ {test_name} test failed")
    
    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Monitor is ready to use.")
        return True
    else:
        print("⚠️ Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 